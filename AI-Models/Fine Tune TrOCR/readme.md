# **Fine-Tuning TrOCR for Arabic and English Handwritten Text Recognition**

This module focuses on fine-tuning the [TrOCR](https://huggingface.co/microsoft/trocr-base-handwritten) model for recognizing Arabic and English handwritten text at the **word level**, a crucial step in the broader Pen-to-Pill pipeline.

---

## **Dataset Location** 

- **Annotated words Dataset**: [View Dataset on Roboflow](https://universe.roboflow.com/handwritten-annotation/word-annotation)


- The [**training image dataset**](https://drive.google.com/drive/folders/16UwlqoQHIbKbaId0BsbIIF1qUIP8hVNK?usp=sharing) used for fine-tuning is stored on Google Drive.

- the label file that contains each image with its word (path to file in github)
Here’s an enhanced and more professional version of your **Dataset Location (Google Drive)** section for the README file, improving clarity, structure, and consistency:

---

## Dataset Location

To fine-tune the TrOCR model on Arabic handwritten word images, we used both annotated data and a labeled image dataset. Here's where you can access the resources:

* **1. Annotated Words Dataset** (Bounding Box Annotation for Each Word):
  
  [🔗 View on Roboflow](https://universe.roboflow.com/handwritten-annotation/word-annotation)
  This dataset was used to train the YOLO model to detect word-level bounding boxes.

* **2. Training Image Dataset** (Used for TrOCR Fine-Tuning):
  
  [🔗 Google Drive Folder](https://drive.google.com/drive/folders/16UwlqoQHIbKbaId0BsbIIF1qUIP8hVNK?usp=sharing)
  Contains pre-cropped handwritten word images prepared for TrOCR training.

* **3. Label File** (Image-to-Word Mappings):
  [TROCR-Labels.xlsx](https://github.com/HabibaYossre/Pen-To-Pill/AI-Models/Fine Tune TrOCR/ Model Fine-tuning/TROCR-Labels.xlsx)
  This Excel file contains two columns:

  * `image`: name of the image file
  * `word`: corresponding handwritten word

---

