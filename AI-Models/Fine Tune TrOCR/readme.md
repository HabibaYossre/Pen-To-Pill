# **Fine-Tuning TrOCR for Arabic and English Handwritten Text Recognition**

This module focuses on fine-tuning the [TrOCR](https://huggingface.co/microsoft/trocr-base-handwritten) model for recognizing Arabic and English handwritten text at the **word level**, a crucial step in the broader Pen-to-Pill pipeline.

---

## Dataset Location

To fine-tune the TrOCR model on Arabic handwritten word images, we used both annotated data and a labeled image dataset. Here's where you can access the resources:

* **1. Annotated Words Dataset** (Bounding Box Annotation for Each Word):
  
  [🔗 View on Roboflow](https://universe.roboflow.com/handwritten-annotation/word-annotation)
  This dataset was used to train the YOLO model to detect word-level bounding boxes.

* **2. Training Image Dataset** (Used for TrOCR Fine-Tuning):
  
  [🔗 Google Drive Folder](https://drive.google.com/drive/folders/1lawEwlqBepyscLwgvwBQVeLdBfjplsrs?usp=sharing)
  Contains pre-cropped handwritten word images prepared for TrOCR training.

* **3. Label File** (Image-to-Word Mappings):
  [TROCR-Labels.xlsx](https://github.com/HabibaYossre/Pen-To-Pill/blob/main/AI-Models/Fine%20Tune%20TrOCR/Model%20Fine-tuning/TROCR-Labels.xlsx)
  This Excel file contains two columns:

  * `image`: name of the image file
  * `word`: corresponding handwritten word

---

## **Steps Overview**

### **1️. Data Collection & Preparation**

* Handwritten word images were **manually labeled** after being cropped using YOLO-detected bounding boxes.

* For each cropped image, the **corresponding ground truth** word was assigned through manual annotation.

* All labeled word images were then consolidated into a single directory, forming a clean and **structured dataset** ready for TrOCR fine-tuning.

> This process ensures high-quality training data by combining automated detection with manual correction for optimal accuracy.

---

### **2️. Model Fine-Tuning**

* **Model & Processor**: Used the pre-trained `microsoft/trocr-base-handwritten` model with `TrOCRProcessor` to handle English and Arabic handwritten word recognition.

* **Data Pipeline**: Loaded images and corresponding word labels from an Excel file and image folder, then created custom `PrescriptionDataset` for PyTorch, including text tokenization and image processing.

* **Training Setup**: Fine-tuned the model using `Seq2SeqTrainer` from Hugging Face with evaluation at every 200 steps, a custom Character Error Rate (CER) metric, and memory optimizations tailored for low-resource environments.


---

## **Evaluation & Metrics**

![Rough Metrics](./Model%20Fine-tuning/accuracy.png)


---

##  **Results**

| Metric         | Value                               |
| -------------- | ----------------------------------- |
| **Exact match accuracy** | **80%** |
| **Character Level accuracy**  | **83.43%** |

---


