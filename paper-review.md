## [Leveraging Deep Learning with Multi-Head Attention for Accurate Extraction of Medicine from Handwritten Prescriptions](https://arxiv.org/html/2412.18199v1)


---

## **1. Abstract (Summary of the Study)**
- The paper focuses on extracting medicine names from **handwritten prescriptions**—a difficult task due to inconsistent handwriting styles.
- A **hybrid approach** is used, combining:
  - **Mask R-CNN** → Segments prescription images to isolate the medicine names.
  - **TrOCR (Transformer-based OCR)** → Converts the segmented handwritten text into digital text.
  - **Multi-Head Attention & Positional Embeddings** → Improves recognition accuracy.
- A **new dataset** of handwritten prescriptions from Pakistan was used to train the model.
- Achieved a **Character Error Rate (CER) of 1.4%**, making it a reliable solution.

---

## **2. Introduction (Problem Statement & Contributions)**
### **The Problem**
- **Handwritten prescriptions are difficult to read**, causing confusion for patients and pharmacists.
- Existing OCR techniques (**CNNs, RNNs, BiLSTM, CTC**) struggle with **blurry, distorted, or highly variable handwriting**.
- Many models require extensive **pre-processing and post-processing**, making them inefficient.

### **The Proposed Solution**
1. **A Hybrid Model:** 
   - **Mask R-CNN** segments medicine name regions.
   - **TrOCR** (Transformer-based OCR) transcribes the text.
   - **String matching techniques** match the extracted text with a database of medicine names.
2. **A New Dataset:** 
   - Collected **handwritten prescriptions from Pakistan** to train the model for diverse handwriting styles.

---

## **3. Literature Review (Previous Work & Limitations)**
- **OCR Approaches:** Various methods have been tested, such as:
  - **CNN + BiLSTM + CTC:** Works well but fails on blurry images.
  - **CRNN (CNN + RNN):** Good for sequence-based text but lacks robustness for real-world handwriting.
  - **Support Vector Machines (SVM):** Used for structured documents like bank cheques but struggles with unstructured handwritten text.
  - **Tesseract OCR:** Computationally expensive and slow for complex handwriting.
  - **Deep Learning-Based OCR (CRNN, TrOCR, Mask R-CNN):** 
    - TrOCR outperforms older models by using **Transformers** instead of CNN + RNN.
    - Mask R-CNN helps isolate regions of interest in prescriptions.

---

## **4. Dataset and Description**
### **Image Dataset**
- **Collected 1,000 handwritten prescriptions** from **50 doctors across Pakistan** (with consent).
- Applied **data augmentation** to increase dataset size to **9,920 images**, including:
  - **Brightness adjustment, contrast normalization, translation, shearing, elastic transformation, Gaussian noise, cropping, padding.**
- Ensured the dataset had **diverse handwriting styles and formats**.

---

## **5. Proposed Methodology (How the Model Works)**
### **Step 1: Image Processing with Mask R-CNN**
- **Uses ResNet-50 with Feature Pyramid Network (FPN)** to extract medicine name regions from prescriptions.
- **Region Proposal Network (RPN)** detects candidate areas where text might be present.

### **Step 2: Text Recognition with TrOCR**
- **TrOCR** converts the handwritten medicine names into digital text.
- Uses **Multi-Head Attention & Positional Embeddings** for better accuracy.

### **Step 3: Post-Processing**
- The recognized text is compared with an **existing medicine database** to match the correct name.
- **Hybrid String Matching** is used to correct errors in spelling or recognition.

---

### **Key Takeaways**
- The study **solves a real-world problem** by extracting medicine names from messy handwritten prescriptions.
- It **improves OCR accuracy** using **Mask R-CNN + TrOCR + Multi-Head Attention**.
- The **custom dataset** from Pakistan makes the model robust to **regional handwriting variations**.
- **Achieved 1.4% Character Error Rate (CER)**, making it **one of the most accurate OCR solutions for handwritten prescriptions**.

---

Would you like me to summarize the remaining sections or explain any part in more detail? 😊