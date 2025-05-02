from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import torch
from PIL import Image, ImageEnhance
from transformers import AutoProcessor, VisionEncoderDecoderModel, BartTokenizer, BartForConditionalGeneration
from typing import List, Dict, Tuple, Any
import io
import tempfile
import os
import uvicorn
from ultralytics import YOLO
import shutil
from fastapi.middleware.cors import CORSMiddleware


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
device = "cuda" if torch.cuda.is_available() else "cpu"
model = None  # YOLO model
processor = None  # TrOCR processor
new_model = None  # TrOCR model
bart_tokenizer = None
bart_model = None

@app.on_event("startup")
async def load_models():
    global model, processor, new_model, bart_tokenizer, bart_model
    
    print("Loading models...")
    model_path = "haneenakram/trocr_finetune_weights_stp"
    
    try:
        from huggingface_hub import HfApi, hf_hub_download
        import torch
        from transformers import VisionEncoderDecoderModel, AutoProcessor
        
        api = HfApi()
        
        # List files in the repository to check the correct path
        files = api.list_repo_files(model_path)
        print(f"Available files in repo: {files}")
        
        # Load YOLO model
        try:
            # Find the YOLO model file
            yolo_path = hf_hub_download(repo_id=model_path, filename="model/yolo_model.pt")
            print(f"Downloaded YOLO weights from {yolo_path}")
            
            # YOLO requires .pt extension, so we need to create a copy with the correct extension
            temp_dir = tempfile.mkdtemp()
            yolo_copy_path = os.path.join(temp_dir, "yolo_model.pt")
            shutil.copy(yolo_path, yolo_copy_path)
            print(f"Created copy with .pt extension at {yolo_copy_path}")
            
            # Load YOLO model from the copied file
            # The key fix is to use the correct model loading method for custom models
            model = YOLO(yolo_copy_path)
            print(f"YOLO model loaded successfully")
            
        except Exception as e:
            print(f"Error loading YOLO model: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # DIRECT FIX - If the YOLO model needs to be initialized from a different format:
            # Try alternative approach using custom class
            try:
                print("Attempting alternative YOLO loading method...")
                # Create a custom YOLO instance without loading weights yet
                model = YOLO("yolov8n.pt")  # Start with a base model
                
                # Load the weights manually
                state_dict = torch.load(yolo_path, map_location="cpu")
                
                # Apply weights to the model
                model.model.load_state_dict(state_dict)
                print("Successfully loaded YOLO model with alternative method")
            except Exception as alt_e:
                print(f"Alternative YOLO loading method failed: {str(alt_e)}")
                traceback.print_exc()
        
        # Initialize new_model to None so we can check if it's loaded later
        new_model = None
        
        # Load TrOCR model
        try:
            # First load the base processor
            processor = AutoProcessor.from_pretrained("microsoft/trocr-base-handwritten")
            print("TrOCR processor loaded from microsoft/trocr-base-handwritten")
            
            # Load the base model architecture first
            print("Loading base TrOCR model architecture from microsoft/trocr-base-handwritten...")
            try:
                new_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
                print("Base TrOCR model architecture loaded successfully")
                
                # Check if the model was loaded properly
                if new_model is None:
                    raise ValueError("Failed to load base model - returned None")
                
                # Specifically look for model.pth inside the model folder
                if "model/model.pth" in files:
                    print("Found model.pth in the model folder")
                    # Download the weights file
                    weights_path = hf_hub_download(repo_id=model_path, filename="model/model.pth")
                    print(f"Downloaded weights from {weights_path}")
                    
                    # Load the state dict
                    state_dict = torch.load(weights_path, map_location="cpu")
                    print(f"State dict loaded, keys: {state_dict.keys() if isinstance(state_dict, dict) else 'not a dictionary'}")
                    
                    # Handle potential differences in state dict keys
                    if isinstance(state_dict, dict) and "state_dict" in state_dict:
                        state_dict = state_dict["state_dict"]
                        print("Extracted state_dict from the loaded file")
                    
                    # Print some debugging info about the state dict
                    if isinstance(state_dict, dict):
                        print(f"State dict contains {len(state_dict)} keys")
                        # Print a few sample keys to help with debugging
                        sample_keys = list(state_dict.keys())[:5]
                        print(f"Sample keys: {sample_keys}")
                        
                        # Only access the model's state_dict if it exists
                        if new_model is not None:
                            model_state = new_model.state_dict()
                            model_sample_keys = list(model_state.keys())[:5]
                            print(f"Model state dict sample keys: {model_sample_keys}")
                    
                    # Try to load the state dict, ignoring mismatched keys
                    try:
                        missing_keys, unexpected_keys = new_model.load_state_dict(state_dict, strict=False)
                        print(f"Custom weights loaded with {len(missing_keys)} missing keys and {len(unexpected_keys)} unexpected keys")
                        if missing_keys:
                            print(f"Sample missing keys: {missing_keys[:5]}")
                        if unexpected_keys:
                            print(f"Sample unexpected keys: {unexpected_keys[:5]}")
                    except Exception as load_error:
                        print(f"Error loading state dict: {str(load_error)}")
                        
                        # If direct loading failed, try to map the keys manually
                        print("Attempting to map keys manually...")
                        new_state_dict = {}
                        
                        # Only proceed if we have a valid model and state_dict
                        if new_model is not None and isinstance(state_dict, dict):
                            # Check if we have encoder/decoder structure or flattened structure
                            has_encoder_prefix = any("encoder" in k for k in state_dict.keys())
                            
                            if has_encoder_prefix:
                                # Keys already have encoder/decoder prefixes
                                new_state_dict = state_dict
                            else:
                                # We need to guess the mapping based on tensor shapes
                                model_state = new_model.state_dict()
                                
                                for key, value in state_dict.items():
                                    # Try to find matching parameters by shape
                                    for model_key, model_param in model_state.items():
                                        if value.shape == model_param.shape:
                                            new_state_dict[model_key] = value
                                            break
                            
                            # Try loading with the mapped dictionary
                            if new_state_dict:
                                missing, unexpected = new_model.load_state_dict(new_state_dict, strict=False)
                                print(f"Mapped weights loaded with {len(missing)} missing keys and {len(unexpected)} unexpected keys")
                else:
                    print("model/model.pth not found in files. Available files:", files)
                
                # Move model to the appropriate device if it's loaded successfully
                if new_model is not None:
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    new_model.to(device)
                    print(f"Model moved to device: {device}")
                else:
                    print("Cannot move model to device because model is None")
                
            except Exception as model_load_error:
                print(f"Error loading base TrOCR model: {str(model_load_error)}")
                import traceback
                traceback.print_exc()
                
        except Exception as e:
            print(f"Error in TrOCR loading process: {str(e)}")
            import traceback
            traceback.print_exc()
        # # Load BART for text correction
        # try:
        #     print("Loading BART model...")
        #     bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
        #     bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")
        #     bart_model.to(device)
        #     print("BART model loaded successfully")
        # except Exception as e:
        #     print(f"Error loading BART model: {str(e)}")
        #     bart_tokenizer = None
        #     bart_model = None

    except Exception as e:
        print(f"Error accessing Hugging Face repository: {str(e)}")
        import traceback
        traceback.print_exc()
        
    print("Model loading completed")
    print(f"YOLO model loaded: {model is not None}")
    print(f"TrOCR model loaded: {new_model is not None}")
    print(f"BART model loaded: {bart_model is not None}")
    
    # If models failed to load, we should report this clearly
    if new_model is None:
        print("WARNING: TrOCR model failed to load! Application will not function correctly.")
    if model is None:
        print("WARNING: YOLO model failed to load! Application will not function correctly.")
    if bart_model is None:
        print("WARNING: BART model failed to load! Text correction will be skipped.")

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
    # If BART model or tokenizer isn't loaded, just return the original texts
    if tokenizer is None or model is None:
        return texts
        
    corrected_texts = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True).to(device)
        with torch.no_grad():
            summary_ids = model.generate(inputs['input_ids'], max_length=1024, num_beams=4, early_stopping=True)
        corrected_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        corrected_texts.append(corrected_text)
    return corrected_texts

def split_into_medicine_dosage_pairs(corrected_text):
    pairs = []
    items = [item.strip() for item in corrected_text.split(',') if item.strip()]
    for item in items:
        parts = item.strip().split(maxsplit=1)
        if len(parts) == 2:
            medicine, dosage = parts
            pairs.append((medicine, dosage))
        else:
            pairs.append((parts[0], ""))
    return pairs

def process_image(image):
    # Check if models are loaded
    if model is None or new_model is None:
        raise Exception("Models not loaded properly. Please check server logs.")
        
    # Run YOLO model for text detection
    yolo_results = model(image)
    
    # Extract boxes
    boxes = []
    for result in yolo_results:
        boxes.extend(result.boxes.xyxy.cpu().numpy())
    
    # Process boxes
    boxes = remove_duplicate_boxes(boxes)
    sorted_boxes = sort_boxes_top_to_bottom_left_to_right(boxes)
    
    # Extract text from each box
    extracted_text = ""
    for box in sorted_boxes:
        x1, y1, x2, y2 = map(int, box)
        cropped_image = image[y1:y2, x1:x2]
        trocr_input = preprocess_for_trocr(cropped_image)
        inputs = {k: v.to(device) for k, v in processor(images=trocr_input, return_tensors="pt").items()}
        with torch.no_grad():
            generated_ids = new_model.generate(**inputs)
            output_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        extracted_text += output_text.strip() + " "
    
    # Correct text using BART if it's available
    if bart_tokenizer is not None and bart_model is not None:
        corrected_texts = correct_text_with_bart([extracted_text.strip()], 
                                                bart_tokenizer, 
                                                bart_model, 
                                                device)
    else:
        # Skip BART correction if not available
        corrected_texts = [extracted_text.strip()]
    
    # Split into medicine-dosage pairs
    return split_into_medicine_dosage_pairs(corrected_texts[0])

@app.get("/")
def read_root():
    return {"message": "Prescription OCR API is running. Send a POST request to /process_prescription/ with an image file."}

@app.post("/process_prescription/")
async def process_prescription(file: UploadFile = File(...)):
    # Check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read the image file
    contents = await file.read()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
        temp.write(contents)
        temp_path = temp.name
    
    try:
        # Read the image with OpenCV
        image = cv2.imread(temp_path)
        if image is None:
            raise HTTPException(status_code=400, detail="Could not read image file")
        
        # Process the image
        results = process_image(image)
        
        # Format results
        formatted_results = [{"medicine": medicine, "dosage": dosage} for medicine, dosage in results]
        
        return JSONResponse(content={"prescriptions": formatted_results})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)