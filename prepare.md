## 1. Introduction

The **Handwritten Extraction** task in **Machathon 6.0** focuses on developing an AI model to extract and interpret handwritten text from **prescription images**. The goal is to create a system that accurately identifies and digitizes handwritten medical prescriptions, ignoring printed text and irrelevant layout details.

## 2. Problem Definition

- Input: Prescription images with handwritten text in:
  - Fully Arabic
  - Fully English
  - Mixed (Arabic & English)
- Challenges:
  - Extracting **only** the handwritten portion.
  - Handling **mixed scripts** (Arabic + English in one image).
  - Addressing **misspellings** and OCR **extraction errors**.
  - Ignoring **irrelevant printed text** (doctor details, hospital name, headers).
- Evaluation Metrics:
  - **Word Error Rate (WER)**
  - **Character Error Rate (CER)**
  - **Model Efficiency** (lightweight, non-redundant model)

## 3. Proposed Solution

### 3.1. Data Preparation

- **Dataset Collection**:
  - Handwritten medical prescription datasets.
  - Synthetic datasets with **real-world handwriting samples**.
- **Preprocessing Techniques**:
  - **Grayscale conversion**.
  - **Thresholding** (Otsu’s method, Adaptive thresholding).
  - **Noise removal** (Morphological operations, Gaussian filtering).
  - **Deskewing and Line Segmentation** (Hough Transform, Projection Profile Analysis).

### 3.2. Model Selection

We will explore multiple OCR approaches:

#### (A) **Traditional OCR - Baseline**

- **Tesseract OCR** (Fine-tuned for Arabic & English handwriting)

#### (B) **Deep Learning-Based OCR**

- **CNN + RNN + CTC Loss (CRNN Model)**:
  - CNNs for **feature extraction**.
  - RNNs (LSTMs/GRUs) for **sequence modeling**.
  - **CTC (Connectionist Temporal Classification) Loss** for end-to-end text recognition.
- **Transformer-based OCR**:
  - **TrOCR (Transformer-based OCR)** for handwritten text recognition.

### 3.3. Model Training & Fine-Tuning

- **Data Augmentation** (Rotation, Scaling, Noise addition, Contrast adjustment).
- **Training Loss**: CTC Loss for sequence-to-sequence learning.
- **Optimization**: Adam optimizer with learning rate decay.

### 3.4. Post-Processing

- **Language Models (BERT, GPT-3, CAMeL)** for error correction.
- **Custom Rule-Based Filtering** to remove unwanted printed text.
- **Dictionary-based spelling correction**.

## 4. Implementation Steps

### Step 1: Preprocessing

- Convert images to grayscale.
- Apply adaptive thresholding.
- Remove noise using OpenCV.

### Step 2: Model Training

- Fine-tune a **CRNN** or **TrOCR** model on labeled dataset.
- Train with CTC Loss for better handwritten text alignment.

### Step 3: Evaluation

- Validate the model using **WER** and **CER**.
- Compare results with baseline OCR methods.

### Step 4: Deployment

- Convert the trained model into an **API** (Flask/FastAPI).
- Optimize for **mobile and web** integration.

## 5. Conclusion

This document outlines the **Handwritten Extraction** process for Machathon 6.0, from **problem definition** to **model deployment**. The focus is on leveraging **OCR, Deep Learning, and NLP** to create an efficient and accurate **handwriting recognition system** tailored for **medical prescriptions**.
