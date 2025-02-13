- **Challenges**:

    - Extracting text only from the handwritten portion of the prescription.
    - Handling mixed-script prescriptions.
    - Addressing misspellings and Extraction errors. //nlp
    - Ignoring redundant layout information such as doctor details, hospital headers, and printed text

- before extraction process, there is a model based solution to differ from printed and handwritten


## Implementation Pipeline

- **Step 1**: Preprocess the image (binarization, noise removal, skew correction).

- **Step 2**: Detect script type (Arabic, English, or mixed).

- **Step 3**: Segment handwritten text using ocr or a deep learning model.

- **Step 4**: Recognize text using a CRNN model with CTC loss.

- **Step 5**: Post-process the text (normalization, error correction, redundant information removal).

- **Step 6**: Evaluate the output using WER, CER, and model efficiency metrics.

---

## **Phase 1: Image Processing & Segmentation**

1. Feature Extraction (ResNet-50 + Feature Pyramid Network)

    - extracts important features from prescription images.

    - To detect objects at different sizes.

2. Identifying Regions with Text (Region Proposal Network - RPN)

    - The RPN scans the extracted features to suggest possible areas where medicine names are present.
    Each proposed area is called an "anchor box" and has:

        - Objectness Score – Probability of containing text.
        - Bounding Box Coordinates – Position of the text region.

3. Refining Detected Regions (RoI Align)

- Since RPN’s bounding boxes may not be precise, RoI Align adjusts them for better accuracy.

4. Segmentation (Mask R-CNN)

## Phase 2: Handwritten Text Recognition & Matching

1. **Handwritten Text Recognition (TrOCR)**
    - TrOCR converts segmented images into text using a Transformer-based Vision Model (ViT).

2. Matching Recognized Text with Medicine Database


- Deep Learning for Image Processing (ResNet-50 + FPN + RPN + RoI Align + Mask R-CNN)
- Transformer-based Handwriting Recognition (TrOCR)
- Hybrid String Matching for Accuracy