
# 📘 mBART-Based Models for Text Correction, Medicine Extraction, and Dosage Extraction

This document describes the three fine-tuned **BART models** used in the **Pen to Pill** system — an AI-powered solution for structuring and understanding handwritten medical prescriptions.

---

## 🧠 Overview of Models

| Model # | Task                      | Input                                 | Output                                    |
|--------|---------------------------|---------------------------------------|-------------------------------------------|
| 1      | Correction & Structuring  | OCR text from TrOCR (`Extracted Text`) | Structured: "medicine dosage, ..."       |
| 2      | Medicine Extraction       | Structured text (`Prescription`)       | "medicine1, medicine2, ..."               |
| 3      | Dosage Extraction         | Structured text (`Prescription`)       | "dosage1, dosage2, ..."                   |

---

## 📁 Data Columns from `mBartPredictions.csv`

| Model | Input Column       | Output Column     |
|-------|---------------------|-------------------|
| 1     | `Extracted Text`    | `Prescription`    |
| 2     | `Prescription`      | `Medicine`        |
| 3     | `Prescription`      | `Appointment`     |

---

## ✳️ Model 1: Correction and Structuring

### ✅ Objective

Transform noisy TrOCR text into a clean, structured format:  
`"medicine1 dosage1, medicine2 dosage2, ..."`

### 🧾 Example

```text
Input:
Cefixime Every hours 6 باراسيتامول hours Every 8 كاربوسيستين daily Twice

Output:
Cefixime Every 6 hours, باراسيتامول Every 8 hours, كاربوسيستين Twice daily
```
## ✳️ Model 2: Medicine Name Extraction

### ✅ Objective

Extract only **medicine names** from the structured prescription.

### 🧾 Example

```text
Input:
Cefixime Every 6 hours, باراسيتامول Every 8 hours, كاربوسيستين Twice daily

Output:
Cefixime, باراسيتامول, كاربوسيستين`
```
## ✳️ Model 3: Dosage Extraction

### ✅ Objective

Extract only **dosages and timings** from the structured prescription.

### 🧾 Example

```text
Input:
Cefixime Every 6 hours, باراسيتامول Every 8 hours, كاربوسيستين Twice daily

Output:
Every 6 hours, Every 8 hours, Twice daily`
```