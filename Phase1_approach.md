The goal is to extract only handwritten text from prescription images while handling fully Arabic, fully English, and mixed-script text. Additionally, the system should ignore printed text, doctor details, and headers.


phase workflow:

1. Task 1: Classify printed and handwritten text in medical prescriptions

    - Step 1: Locate text regions in the prescription.
    - Step 2: Categorize them as handwritten, printed, mixed, or non-text using a Random Forest classifier.
    
2. Task 2: Extract medicine names and dosages from handwritten prescriptions.


Notes from papers:

- Transformers[20] can also be used instead or along with
traditional DL models that are currently being used in the literature, in one scenario we can replace the whole **CRNN**
model with the **transformers** or we can also just replace the **RNN** part of the CRNN (CNN+RNN) model with
**transformers** as transformers perform much better than traditional RNN models like LSTM , GUR, etc.


Approach 1: Image Processing & Segmentation
1.	Preprocessing: Convert images to grayscale, remove noise, and correct skew.
2.	Detect Script Type: Classify prescriptions as Arabic, English, or mixed using a CNN-based classifier.
3.	Feature Extraction: Use ResNet-50 + FPN to detect and extract relevant text features.
4.	Text Region Identification: Apply RPN to propose text regions and refine them using RoI Align.
5.	Segmentation: Use Mask R-CNN to isolate handwritten text from printed elements.
Approach 2: Handwritten Text Recognition & Matching
1.	Handwritten Text Recognition: Use TrOCR (Transformer-based OCR) to convert segmented images into text.
2.	Text Recognition with CRNN + CTC Loss: Recognize and align text sequences.
3.	Post-processing: Correct errors using language models (BERT, GPT-3, CAMeL) and dictionary-based verification.
Text Matching: Validate extracted medicine names against a medical database using hybrid string-matching.
