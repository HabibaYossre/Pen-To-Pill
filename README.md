# 🩺 **Pen to Pill (P2P) - Prescription Digitization System**

> **Summit Machathon 6.0 Project**  
> Team Members: Habiba Yousri, Haneen Akram, Renad Hossam, Mohammed Mostafa, Shrouk Mohamed

---

## **Overview**

**Pen to Pill (P2P)** is an AI-powered system that digitizes handwritten medical prescriptions, with a focus on complex multilingual documents written in Arabic and English. It aims to improve patient safety and healthcare efficiency by extracting structured medication data from unstructured, handwritten prescriptions.


---

## **Tools & Technologies**

- **Roboflow** – Annotation tool for labeling Arabic and English words.
- **YOLOv8** – Detects handwritten regions in prescriptions.
- **TrOCR** – Transformer-based OCR for recognizing multilingual handwriting.
- **BART (mBART)** – Corrects and structures extracted text into a standard format.
- **Python**, **PyTorch** – Core implementation frameworks.
- **Google Colab / Kaggle Notebooks** – Training & experimentation environments.
- **React.js** – Frontend library for building the user interface.
- **FastAPI** – High-performance web framework for building the backend API.

---

## 🔍 **Methodology**

The solution follows a multi-step pipeline:

1. **Handwritten Word Region Detection**
   - Custom annotations using Roboflow.
   - YOLOv8 model trained to detect word-level bounding boxes (Arabic & English).

2. **Duplicate Box Removal**
   - Non-Maximum Suppression (IoU = 0.8) to eliminate redundant detections.

3. **Box Sorting**
   - Sort boxes top-to-bottom, left-to-right for proper text sequence.

4. **Text Recognition (TrOCR)**
   - Preprocessed and resized word images.
   - Fine-tuned TrOCR model for accurate handwriting recognition.

5. **Text Reconstruction**
   - Combine individual words into a single prescription string.

6. **Text Correction & Structuring (BART)**
   - Clean and format OCR output into: `medicine dosage, medicine dosage, ...`

7. **Post-Processing**
   - Extract `(medicine, dosage)` pairs for digital use.

---

##  **Future Work**

- Expand the dataset with more real-world handwritten prescriptions.
- Improve mBART output consistency on edge cases.
- Integrate with digital health record systems and mobile applications.
- Extend multilingual support beyond Arabic-English.

---

## **Installation & Deployment Guide**

### Prerequisites
- Node.js and npm installed
- Python 3.10 installed
- Git installed

### Installation & Setup

#### Frontend Setup
1. Navigate to the Frontend directory:
   ```bash
   cd FrontEnd
   ```

2. Install dependencies:
   ```bash
   npm i
   ```

3. Start the development server:
   ```bash
   npm run server
   ```

4. In a new terminal, start the React application:
   ```bash
   npm start
   ```

#### Backend Setup
1. Navigate back to the project root directory, then to the Backend folder:
   ```bash
   cd ..
   cd BackEnd
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

The frontend application should now be accessible at `http://localhost:8000` and will communicate with the backend running on the port specified in the FastAPI application.

