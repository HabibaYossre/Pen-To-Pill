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

app = FastAPI(
    title="Prescription OCR API",
    description="API for extracting medicine and dosage information from prescription images",
    version="1.0.0"
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
    # Load YOLO model for text detection
    # For YOLO, we need to handle the path differently
    # model = YOLO("yolov8n.pt")  # First load a base model
    model_path = "haneenakram/trocr_finetune_weights_stp"
    
    try:
        from huggingface_hub import HfApi
        from huggingface_hub import hf_hub_download
        api = HfApi()
        
        # List files in the repository to check the correct path
        files = api.list_repo_files(model_path)
        print(f"Available files in repo: {files}")
        # Find the YOLO model file        
        yolo_path = hf_hub_download(repo_id=model_path, filename="model/yolo_model.pth")
        model = YOLO(yolo_path)
        print(f"YOLO model loaded from {yolo_path}")
        
    except Exception as e:
        print(f"Error loading YOLO model: {str(e)}")
    
    # Load TrOCR for text recognition
    try:
        processor = AutoProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        new_model = VisionEncoderDecoderModel.from_pretrained(model_path, subfolder="model")
        new_model.to(device)
        print("TrOCR model loaded successfully")
    except Exception as e:
        print(f"Error loading TrOCR model: {str(e)}")
        # Fallback to base model
        # new_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        # new_model.to(device)
        # print("Falling back to base TrOCR model")
    
    # # Load BART for text correction
    # try:
    #     bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
    #     # Try to load custom BART model if available
    #     bart_model = BartForConditionalGeneration.from_pretrained(model_path, subfolder="model")
    #     bart_model.to(device)
    #     print("Custom BART model loaded successfully")
    # except Exception as e:
    #     print(f"Error loading custom BART model: {str(e)}")
    #     # Fallback to standard BART model
    #     bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")
    #     bart_model.to(device)
    #     print("Falling back to base BART model")
    
    print("All models loaded successfully!")

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
    
    # Correct text using BART
    corrected_texts = correct_text_with_bart([extracted_text.strip()], 
                                             tokenizer=bart_tokenizer, 
                                             model=bart_model, 
                                             device=device)
    
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