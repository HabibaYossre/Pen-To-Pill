from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import torch
from PIL import Image, ImageEnhance
from transformers import AutoProcessor, MBart50Tokenizer, MBartTokenizer, MBartForConditionalGeneration, VisionEncoderDecoderModel, BartTokenizer, BartForConditionalGeneration
from typing import List, Dict, Tuple, Any
import io
import tempfile
import os
import uvicorn
from ultralytics import YOLO
import shutil
from fastapi.middleware.cors import CORSMiddleware

# Initialize device at the beginning
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

app = FastAPI(
    title="Prescription OCR API",
    description="API for extracting medicine and dosage information from prescription images",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variables
model = None  # YOLO model
processor = None  # TrOCR processor
new_model = None  # TrOCR model
bart_tokenizer = None  # MBart for text ordering
bart_model = None
bart_tokenizer_1 = None  # BART for medicine extraction
bart_model_1 = None
bart_tokenizer_2 = None  # BART for dosage extraction
bart_model_2 = None

@app.on_event("startup")
async def load_models():
    global model, processor, new_model, bart_tokenizer, bart_model, bart_tokenizer_1, bart_model_1, bart_tokenizer_2, bart_model_2
    
    print("Starting model loading process...")
    model_path = "haneenakram/trocr_finetune_weights_stp"
    
    # Initialize models to None so we can check if they're loaded later
    model = None  # YOLO
    new_model = None  # TrOCR
    processor = None  # TrOCR processor
    bart_model = None  # MBart for text ordering
    bart_tokenizer = None
    bart_model_1 = None  # BART for medicine extraction
    bart_tokenizer_1 = None
    bart_model_2 = None  # BART for appointment/dosage extraction
    bart_tokenizer_2 = None
    
    try:
        from huggingface_hub import HfApi, hf_hub_download
        import torch
        from transformers import VisionEncoderDecoderModel, AutoProcessor
        
        api = HfApi()
        
        # List files in the repository to check the correct path
        files = api.list_repo_files(model_path)
        print(f"Available files in repo: {files}")
        
        # Determine available devices and memory
        if torch.cuda.is_available():
            print(f"CUDA available: {torch.cuda.get_device_name(0)}")
            try:
                # Check available GPU memory (in MB)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
                free_memory = torch.cuda.memory_reserved(0) / (1024 * 1024)
                print(f"GPU total memory: {gpu_memory:.2f} MB, Free memory: {free_memory:.2f} MB")
                
                # If very limited GPU memory, use CPU for all models
                if gpu_memory < 4000:  # Less than 4GB
                    primary_device = "cpu"
                    secondary_device = "cpu"
                    print("Limited GPU memory detected, using CPU for all models")
                else:
                    primary_device = "cuda"
                    secondary_device = "cpu"  # Use CPU for less critical models
                    print(f"Using GPU for primary models, CPU for secondary models")
            except Exception as e:
                print(f"Error checking GPU memory: {str(e)}")
                primary_device = "cuda" 
                secondary_device = "cpu"
        else:
            primary_device = "cpu"
            secondary_device = "cpu"
            print("CUDA not available, using CPU for all models")
        
        # Convert string device names to torch devices
        primary_device = torch.device(primary_device)
        secondary_device = torch.device(secondary_device)
        
        # Step 1: Load YOLO model (highest priority)
        try:
            print("Loading YOLO model...")
            # Find the YOLO model file
            yolo_path = hf_hub_download(repo_id=model_path, filename="model/yolo_model.pt")
            print(f"Downloaded YOLO weights from {yolo_path}")
            
            # YOLO requires .pt extension, create a copy with the correct extension
            temp_dir = tempfile.mkdtemp()
            yolo_copy_path = os.path.join(temp_dir, "yolo_model.pt")
            shutil.copy(yolo_path, yolo_copy_path)
            
            # Load YOLO model from the copied file
            model = YOLO(yolo_copy_path)
            print("✅ YOLO model loaded successfully")
            
        except Exception as e:
            print(f"Error loading YOLO model: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Try alternative approach using a base model
            try:
                print("Attempting alternative YOLO loading method...")
                model = YOLO("yolov8n.pt")  # Start with a base model
                state_dict = torch.load(yolo_path, map_location="cpu")
                model.model.load_state_dict(state_dict)
                print("✅ Successfully loaded YOLO model with alternative method")
            except Exception as alt_e:
                print(f"❌ Alternative YOLO loading method failed: {str(alt_e)}")
        
        # Step 2: Load TrOCR model (high priority)
        try:
            print("Loading TrOCR processor...")
            processor = AutoProcessor.from_pretrained("microsoft/trocr-base-handwritten")
            print("✅ TrOCR processor loaded successfully")
            
            print("Loading TrOCR model...")
            # Load the base model architecture
            new_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
            
            # Check if custom weights are available
            if "model/model.pth" in files:
                weights_path = hf_hub_download(repo_id=model_path, filename="model/model.pth")
                print(f"Downloaded custom TrOCR weights from {weights_path}")
                
                # Load the state dict
                state_dict = torch.load(weights_path, map_location="cpu")
                
                # Extract state_dict if nested
                if isinstance(state_dict, dict) and "state_dict" in state_dict:
                    state_dict = state_dict["state_dict"]
                
                # Try to load the state dict, ignoring mismatched keys
                try:
                    missing_keys, unexpected_keys = new_model.load_state_dict(state_dict, strict=False)
                    print(f"Custom TrOCR weights loaded with {len(missing_keys)} missing keys")
                except Exception as load_error:
                    print(f"Error loading TrOCR weights: {str(load_error)}")
            
            # Move model to primary device
            new_model = new_model.to(primary_device)
            print(f"✅ TrOCR model loaded successfully on {primary_device}")
            
        except Exception as e:
            print(f"❌ Error loading TrOCR model: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Function to safely load BART models
        def load_bart_model(model_dir, files_prefix, use_mbart=False):
            try:
                # Check if model directory exists
                if not any(f.startswith(f"{files_prefix}/") for f in files):
                    print(f"{files_prefix} directory not found in files")
                    return None, None
                
                print(f"Loading {files_prefix} model...")
                
                # Create temp directory for model files
                temp_dir = os.path.join(tempfile.mkdtemp(), files_prefix)
                os.makedirs(temp_dir, exist_ok=True)
                
                # Get all files in the directory
                model_files = [f for f in files if f.startswith(f"{files_prefix}/")]
                
                # Download essential files first to reduce memory usage
                essential_files = ["config.json", "vocab.json", "tokenizer_config.json", "special_tokens_map.json", "pytorch_model.bin"]
                for filename in essential_files:
                    full_path = f"{files_prefix}/{filename}"
                    if full_path in model_files:
                        file_path = hf_hub_download(repo_id=model_path, filename=full_path)
                        target_path = os.path.join(temp_dir, filename)
                        shutil.copy(file_path, target_path)
                
                # Download remaining files
                for model_file in model_files:
                    if not any(model_file.endswith(f"/{efile}") for efile in essential_files):
                        file_path = hf_hub_download(repo_id=model_path, filename=model_file)
                        target_path = os.path.join(temp_dir, os.path.basename(model_file))
                        shutil.copy(file_path, target_path)
                
                # Choose the appropriate device for this model
                device = secondary_device  # Use secondary device (typically CPU) for BART models
                
                # Load tokenizer and model
                if use_mbart:
                    tokenizer = MBart50Tokenizer.from_pretrained(temp_dir)
                    model = MBartForConditionalGeneration.from_pretrained(temp_dir)
                else:
                    tokenizer = BartTokenizer.from_pretrained(temp_dir)
                    model = BartForConditionalGeneration.from_pretrained(temp_dir)
                
                # Move model to device
                model = model.to(device)
                print(f"✅ {files_prefix} model loaded successfully on {device}")
                
                # Clean up GPU memory if needed
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                return tokenizer, model
                
            except Exception as e:
                print(f"❌ Error loading {files_prefix} model: {str(e)}")
                import traceback
                traceback.print_exc()
                return None, None
        
        # Step 3: Load BART models one at a time (medium priority)
        # This sequential loading helps prevent memory issues
        
        # Load MBart model (for text ordering)
        print("\nStarting to load BART models sequentially")
        bart_tokenizer, bart_model = load_bart_model("mbart", "mbart", use_mbart=True)
        
        # Load BART model 1 (medicine extraction)
        bart_tokenizer_1, bart_model_1 = load_bart_model("medicinembart", "medicinembart")
        
        # Load BART model 2 (appointment/dosage extraction)
        bart_tokenizer_2, bart_model_2 = load_bart_model("Appointmbart", "Appointmbart")

    except Exception as e:
        print(f"Error accessing Hugging Face repository: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Final status report
    print("\n=== Model Loading Summary ===")
    print(f"YOLO model: {'✅ Loaded' if model is not None else '❌ Failed'}")
    print(f"TrOCR model: {'✅ Loaded' if new_model is not None else '❌ Failed'}")
    print(f"MBart model: {'✅ Loaded' if bart_model is not None else '❌ Failed'}")
    print(f"BART model 1: {'✅ Loaded' if bart_model_1 is not None else '❌ Failed'}")
    print(f"BART model 2: {'✅ Loaded' if bart_model_2 is not None else '❌ Failed'}")
    
    # Check if core models are loaded
    if new_model is None or model is None:
        print("\n⚠️ WARNING: Core models failed to load! Application will not function correctly.")

def remove_duplicate_boxes(boxes, iou_threshold=0.8):
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    indices = np.argsort(y2)
    keep = []
    while len(indices) > 0:
        last = len(indices) - 1
        i = indices[last]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[indices[:last]])
        yy1 = np.maximum(y1[i], y1[indices[:last]])
        xx2 = np.minimum(x2[i], x2[indices[:last]])
        yy2 = np.minimum(y2[i], y2[indices[:last]])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / areas[indices[:last]]
        indices = np.delete(indices, np.concatenate(([last], np.where(overlap > iou_threshold)[0])))
    return boxes[keep].tolist()

def sort_boxes_top_to_bottom_left_to_right(boxes):
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    indices = np.lexsort((x1, y1))
    return boxes[indices].tolist()

def preprocess_for_trocr(cropped_image):
    rgb_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    image = pil_image.convert('L')
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    fixed_height = 64
    width_percent = (fixed_height / float(image.size[1]))
    new_width = int((float(image.size[0]) * float(width_percent)))
    image = image.resize((new_width, fixed_height), Image.Resampling.LANCZOS)
    image = image.convert('RGB')
    return image

def correct_text_with_bart(texts, tokenizer, model, device):
    if tokenizer is None or model is None:
        return texts
        
    corrected_texts = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt").to(device)
        with torch.no_grad():
            summary_ids = model.generate(inputs['input_ids'], max_length=1024, num_beams=4, early_stopping=True)
        corrected_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        corrected_texts.append(corrected_text)
    return corrected_texts

def split_into_medicine_dosage_pairs(medicine_text, dosage_text):
    pairs = []
    medicine_items = [item.strip() for item in medicine_text.split(',') if item.strip()]
    dosage_items = [item.strip() for item in dosage_text.split(',') if item.strip()]

    for med, dos in zip(medicine_items, dosage_items):
        pairs.append((med, dos))

    if len(medicine_items) > len(dosage_items):
        for med in medicine_items[len(dosage_items):]:
            pairs.append((med, ""))
    elif len(dosage_items) > len(medicine_items):
        for dos in dosage_items[len(medicine_items):]:
            pairs.append(("", dos))
    return pairs

def process_image(image):
    if model is None or new_model is None:
        raise Exception("Models not loaded properly. Please check server logs.")
        
    # Convert image to GPU if available
    if isinstance(image, np.ndarray):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Run YOLO model
    yolo_results = model(image)
    
    # Extract boxes
    boxes = []
    for result in yolo_results:
        boxes.extend(result.boxes.xyxy.cpu().numpy())
    
    boxes = remove_duplicate_boxes(boxes)
    sorted_boxes = sort_boxes_top_to_bottom_left_to_right(boxes)
    
    extracted_text = ""
    for box in sorted_boxes:
        x1, y1, x2, y2 = map(int, box)
        cropped_image = image[y1:y2, x1:x2]
        trocr_input = preprocess_for_trocr(cropped_image)
        
        # Move inputs to GPU
        inputs = processor(images=trocr_input, return_tensors="pt").to(device)
        
        with torch.no_grad():
            generated_ids = new_model.generate(**inputs)
            output_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        extracted_text += output_text.strip() + " "
    
    # Text processing with BART models
    if bart_tokenizer is not None and bart_model is not None:
        inputs = bart_tokenizer(extracted_text.strip(), return_tensors="pt").to(device)
        with torch.no_grad():
            summary_ids = bart_model.generate(inputs['input_ids'], max_length=1024, num_beams=4, early_stopping=True)
        reordered_text = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    else:
        reordered_text = extracted_text.strip()
    
    if bart_tokenizer_1 is not None and bart_model_1 is not None:
        inputs_med = bart_tokenizer_1(reordered_text, return_tensors="pt").to(device)
        with torch.no_grad():
            med_ids = bart_model_1.generate(inputs_med['input_ids'], max_length=1024, num_beams=4, early_stopping=True)
        medicine_text = bart_tokenizer_1.decode(med_ids[0], skip_special_tokens=True)
    else:
        medicine_text = reordered_text
    
    if bart_tokenizer_2 is not None and bart_model_2 is not None:
        inputs_dos = bart_tokenizer_2(reordered_text, return_tensors="pt").to(device)
        with torch.no_grad():
            dos_ids = bart_model_2.generate(inputs_dos['input_ids'], max_length=1024, num_beams=4, early_stopping=True)
        dosage_text = bart_tokenizer_2.decode(dos_ids[0], skip_special_tokens=True)
    else:
        dosage_text = ""
    
    return split_into_medicine_dosage_pairs(medicine_text, dosage_text)

@app.get("/")
def read_root():
    return {"message": "Prescription OCR API is running. Send a POST request to /process_prescription/ with an image file."}

@app.post("/process_prescription/")
async def process_prescription(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(contents)
        temp_path = temp.name
    
    try:
        image = cv2.imread(temp_path)
        if image is None:
            raise HTTPException(status_code=400, detail="Could not read image file")
        
        results = process_image(image)
        formatted_results = [{"medicine": medicine, "dosage": dosage} for medicine, dosage in results]
        
        return JSONResponse(content={"prescriptions": formatted_results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)