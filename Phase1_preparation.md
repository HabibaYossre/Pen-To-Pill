# Implementation steps:

## preprocessing on prescription images:
- Image Binarization: convert image to `grey scale` and separate text from background
- Noise Reduction: by using `gaussian blur` or `median filter`
- Skew Correction: correct any skew in the image to ensure text is aligned properly
- Layout Analysis: identify and separate handwritten text from printed text

### Code Example:

```python 
import cv2
import numpy as np

# Load the image
image = cv2.imread('prescription.jpg', cv2.IMREAD_GRAYSCALE)

# Binarization: Convert to black and white
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

# Noise Reduction: Apply Gaussian blur
blurred_image = cv2.GaussianBlur(binary_image, (5, 5), 0)

# Skew Correction (example: using Hough Lines)
edges = cv2.Canny(blurred_image, 50, 150, apertureSize=3)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

# Save the preprocessed image
cv2.imwrite('preprocessed_image.jpg', blurred_image)
```

## Extract text using Handwritten Text Recognition (HTR) Models:
- use `CRNN` or `TrOCR`
- handle mixed-script text by translating it all text into arabic
- ignore printed text

### Code Example:
```Python
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# Load the preprocessed image
image = Image.open('preprocessed_image.jpg').convert("RGB")

# Load TrOCR processor and model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

# Preprocess the image and generate text
pixel_values = processor(image, return_tensors="pt").pixel_values
generated_ids = model.generate(pixel_values)
extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print("Extracted Text:", extracted_text)
```

## Correct misspelling:
- use `BERT'S MLM` to predict and correct misspelled words
- `mask each word` in the text and let BERT predict the word
- extract and validate the medicines name with `BioBert` or `clinicalBert`

```python
from transformers import BertTokenizer, BertForMaskedLM
import torch

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

def correct_misspellings(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt')
    
    # Mask every word in the text and get BERT's predictions
    corrected_text = []
    for i, token_id in enumerate(inputs['input_ids'][0]):
        if token_id == tokenizer.mask_token_id:
            continue  # Skip the mask token itself
        
        # Mask the current token
        masked_inputs = inputs['input_ids'].clone()
        masked_inputs[0, i] = tokenizer.mask_token_id
        
        # Get BERT's predictions
        with torch.no_grad():
            outputs = model(masked_inputs).logits
        
        # Decode the predicted token
        predicted_token_id = torch.argmax(outputs[0, i]).item()
        predicted_token = tokenizer.decode(predicted_token_id)
        
        # Add the predicted token to the corrected text
        corrected_text.append(predicted_token)
    
    # Join the corrected tokens into a sentence
    return ' '.join(corrected_text)

# Example usage
text = "Take 2 pills of Parcetamol every 8 hours."
corrected_text = correct_misspellings(text)
print("Corrected Text:", corrected_text)
```

## PostProcessing:
- `remove additional details` that is not necessary (like doctors details).
- `tokenize` the text into words
- we can validate again on the extracted text (optional)

```python
import re

def clean_text(text):
    # Remove irrelevant information (e.g., doctor details, hospital headers)
    cleaned_text = re.sub(r'Dr\.\s\w+', '', text)  # Remove doctor names
    cleaned_text = re.sub(r'Hospital\s\w+', '', cleaned_text)  # Remove hospital names
    
    # Tokenize the text into words
    tokens = cleaned_text.split()
    
    # Validate tokens against a medical dictionary (example)
    medical_dictionary = {"Paracetamol", "Amoxicillin", "Ibuprofen"}
    validated_tokens = [token if token in medical_dictionary else "[UNK]" for token in tokens]
    
    return ' '.join(validated_tokens)

# Example usage
extracted_text = "Take 2 pills of Paracetamol every 8 hours. Dr. Smith, Cairo Hospital."
cleaned_text = clean_text(extracted_text)
print("Cleaned Text:", cleaned_text)
```


