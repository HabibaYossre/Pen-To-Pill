# TrOCR Fine-Tuning for Prescription Words (English + Arabic)

'''
**Dataset Structure:**
- Excel file with columns: `image_name` | `word_label`
- Folder containing all cropped word images
'''

# Install necessary packages (run this in your terminal or notebook if needed)
# !pip install transformers torchvision pandas openpyxl pillow accelerate
import subprocess
subprocess.check_call(["pip", "install", "transformers", "torchvision", "pandas", "openpyxl", "pillow", "accelerate"])

#import libraries
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image
from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer
)
import os

# Load Excel file
df = pd.read_excel("/kaggle/input/excel-file/mohammed file.xlsx")  # Change to your file path
print(f"Loaded {len(df)} samples")
df.head()

# Configuration
IMAGE_FOLDER = "/kaggle/input/cropped-images"  # Change this
TEST_SIZE = 0.1  # 10% for validation
BATCH_SIZE = 8
EPOCHS = 10
MODEL_NAME = "microsoft/trocr-base-handwritten"  # or "microsoft/trocr-base-stage1"

# Create PyTorch Dataset
class PrescriptionDataset(Dataset):
    def __init__(self, df, processor, image_folder):
        self.df = df
        self.processor = processor
        self.image_folder = image_folder

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        # Get image name and label
        img_name = self.df.iloc[idx]['Cropped Image Name']
        text_label = str(self.df.iloc[idx]['word'])
        
        # Load image
        image_path = os.path.join(self.image_folder, img_name)
        image = Image.open(image_path).convert('RGB')

        # Process image and text
        pixel_values = self.processor(image, return_tensors="pt").pixel_values.squeeze()
        labels = self.processor.tokenizer(
            text_label,
            return_tensors="pt",
            padding="max_length",
            max_length=64,
            truncation=True
        ).input_ids.squeeze()

        return {
            "pixel_values": pixel_values,
            "labels": labels
        }
        
# Initialize processor
processor = TrOCRProcessor.from_pretrained(MODEL_NAME)

# Split data
train_df = df.sample(frac=1-TEST_SIZE, random_state=42)
test_df = df.drop(train_df.index)

# Create datasets
train_dataset = PrescriptionDataset(train_df, processor, IMAGE_FOLDER)
eval_dataset = PrescriptionDataset(test_df, processor, IMAGE_FOLDER)

print(f"Train samples: {len(train_dataset)}, Eval samples: {len(eval_dataset)}")

# Initialize model
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)
model.config.decoder_start_token_id = processor.tokenizer.cls_token_id
model.config.pad_token_id = processor.tokenizer.pad_token_id

#Training
training_args = Seq2SeqTrainingArguments(
    output_dir="./",  # Use root directory to avoid nested folders
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    evaluation_strategy="steps",  # More frequent, smaller evaluations
    eval_steps=200,  # Evaluate every 200 steps
    logging_strategy="steps",
    logging_steps=50,
    learning_rate=4e-5,
    num_train_epochs=EPOCHS,
    warmup_ratio=0.1,
    weight_decay=0.01,
    fp16=True if torch.cuda.is_available() else False,
    report_to="none",
    # Disable all saving to conserve space
    save_strategy="no",
    save_total_limit=0,
    load_best_model_at_end=False,
    # Memory/performance optimizations
    gradient_accumulation_steps=2,
    fp16_full_eval=True,
    generation_max_length=64,
    generation_num_beams=1,
    # Kaggle-specific optimizations
    dataloader_pin_memory=False,  # Reduces memory usage
    dataloader_num_workers=2,  # Optimal for Kaggle
)

def compute_metrics(pred):
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    # Clip predictions to valid token ID range
    pred_ids = np.clip(pred_ids, 0, len(processor.tokenizer) - 1)
    
    pred_str = processor.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = processor.tokenizer.pad_token_id
    label_str = processor.batch_decode(labels_ids, skip_special_tokens=True)

    # Calculate character error rate (CER)
    cer = 0
    for pred, label in zip(pred_str, label_str):
        # Simple CER calculation
        cer += sum(1 for a, b in zip(pred, label) if a != b) / max(len(pred), len(label))
    cer /= len(pred_str)

    return {"cer": cer}

# Create trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

# Run training
train_result = trainer.train()

#Test
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
n = 28
# 2. Load test image
for i in range(n):
    test_image_path = os.path.join(IMAGE_FOLDER, test_df.iloc[i]['Cropped Image Name'])
    test_image = Image.open(test_image_path).convert('RGB')
    # 3. Preprocess with device awareness
    with torch.no_grad():
        # Move inputs to same device as model
        pixel_values = processor(test_image, return_tensors="pt").pixel_values.to(device)
        # Generate predictions
        generated_ids = model.generate(pixel_values)
        # Decode results
        predicted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    # 4. Display results
    print("\n=== Prediction Test ===")
    print(f"Image: {test_df.iloc[i]['Cropped Image Name']}")
    print(f"Predicted: {predicted_text}")
    print(f"Actual: {test_df.iloc[i]['word']}")
    # print(f"Match: {predicted_text == test_df.iloc[0]['word']}")