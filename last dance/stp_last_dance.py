# -*- coding: utf-8 -*-

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.
import kagglehub
mohammed237_machathon6_phase1_images_path = kagglehub.dataset_download('mohammed237/machathon6-phase1-images')
mohammed237_merge_file_path = kagglehub.dataset_download('mohammed237/merge-file')
mohammed237_yolo_weights_word_detection_pytorch_default_1_path = kagglehub.model_download('mohammed237/yolo-weights-word-detection/PyTorch/default/1')
mohammed237_trocr_finetune_weights_stp_pytorch_default_1_path = kagglehub.model_download('mohammed237/trocr_finetune_weights_stp/PyTorch/default/1')

print('Data source import complete.')

"""# **Import Libraries**"""

!pip install jiwer
!pip install ultralytics
!pip install fuzzywuzzy

import os
import cv2
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from google.colab import drive
import gdown
from ultralytics import YOLO
import re
from rapidfuzz import fuzz, process
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow
import cv2

"""# **Load YOLO Wieghts**"""

# drive.mount('/content/drive')
# file_id = "1EJRP-VYKdhKxUUcU0U8P6kSyo03SqK3B"
# output = "/content/best.pt"  # Save the file in Colab's working directory
# # Download the file from Google Drive
# gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)
#yoloV8 wieghts
model = YOLO("/kaggle/input/yolo-weights-word-detection/pytorch/default/1/worddetection.pt")  # Path to your downloaded weights

"""# **Declare DB**"""

medicine_list=['Acetazolamide', 'Acetylcysteine', 'Albendazole', 'Amantadine', 'Amoxicillin', 'Artificial Tears', 'Atropine', 'Azithromycin', 'Bimatoprost', 'Botox', 'Brimonidine', 'Calcium Carbonate', 'Carbachol', 'Carbamazepine', 'Carbocisteine', 'Cefdinir', 'Cefixime', 'Cefuroxime', 'Cetirizine', 'Chloramphenicol', 'Chlorhexidine', 'Ciprofloxacin', 'Clindamycin', 'Collagen', 'Cyclosporine', 'Dexamethasone', 'Dextromethorphan', 'Diclofenac', 'Domperidone', 'Donepezil', 'Dorzolamide', 'Doxycycline', 'Erythromycin', 'Fluorometholone', 'Gabapentin', 'Gatifloxacin', 'Glycolic Acid', 'Guaifenesin', 'Hyaluronic Acid', 'Hydrocortisone', 'Hydroquinone', 'Hydroxyzine', 'Ibuprofen', 'Iron Supplements', 'Ketorolac', 'Lactic Acid', 'Latanoprost', 'Levetiracetam', 'Levofloxacin', 'Lidocaine', 'Lifitegrast', 'Loratadine', 'Mannitol', 'Mebendazole', 'Memantine', 'Metoclopramide', 'Metronidazole', 'Montelukast', 'Moxifloxacin', 'Multivitamins', 'Mupirocin', 'Natamycin', 'Nepafenac', 'Niacinamide', 'Nystatin', 'Ofloxacin', 'Omeprazole', 'Ondansetron', 'Oral Rehydration Salts', 'Paracetamol', 'Peptides', 'Pilocarpine', 'Pramipexole', 'Prednisolone', 'Prednisolone Acetate', 'Prednisolone Drops', 'Pregabalin', 'Probiotics', 'Ranitidine', 'Retinol', 'Rivastigmine', 'Ropinirole', 'Salbutamol', 'Salicylic Acid', 'Sodium Hyaluronate', 'Timolol', 'Tobramycin', 'Topiramate', 'Travoprost', 'Tretinoin', 'Tropicamide', 'Valproate', 'Vitamin C Serum', 'Vitamin D', 'Voriconazole', 'Zinc Sulfate', 'أتروبين', 'أزيثروميسين', 'أسيتات البريدنيزولون', 'أسيتازولاميد', 'أسيتيل سيستين', 'ألبيندازول', 'أمانتادين', 'أملاح الإماهة الفموية', 'أموكسيسيلين', 'أوفلوكساسين', 'أوميبرازول', 'أوندانسيترون', 'إريثرومايسين', 'إيبوبروفين', 'الببتيدات', 'البروبيوتيك', 'البوتوكس', 'الفيتامينات المتعددة', 'باراسيتامول', 'براميبيكسول', 'بريجابالين', 'بريدنيزولون', 'بريمونيدين', 'بيلوكاربين', 'بيماتوبروست', 'ترافوبروست', 'تروبيكاميد', 'تريتينوين', 'توبراميسين', 'توبيراميت', 'تيمولول', 'جابابنتين', 'جاتيفلوكساسين', 'حمض الجليكوليك', 'حمض الساليسيليك', 'حمض اللاكتيك', 'حمض الهيالورونيك', 'دموع صناعية', 'دورزولاميد', 'دوكسيسيكلين', 'دومبيريدون', 'دونيبيزيل', 'ديكساميثازون', 'ديكستروميثورفان', 'ديكلوفيناك', 'رانيتيدين', 'روبينيرول', 'ريتينول', 'ريفاستجمين', 'سالبيوتامول', 'سيبروفلوكساسين', 'سيتريزين', 'سيفدينير', 'سيفوريوكسيم', 'سيفيكسيم', 'سيكلوسبورين', 'غوايفينيسين', 'فالبروات', 'فلوروميثولون', 'فوريكونازول', 'فيتامين د', 'قطرات بريدنيزولون', 'كارباشول', 'كاربامازيبين', 'كاربوسيستين', 'كبريتات الزنك', 'كربونات الكالسيوم', 'كلورامفينيكول', 'كلورهيكسيدين', 'كليندامايسين', 'كولاجين', 'كيتورولاك', 'لاتانوبروست', 'لوراتادين', 'ليدوكايين', 'ليفوفلوكساسين', 'ليفيتيجراست', 'ليفيتيراسيتام', 'مانيتول', 'مصل فيتامين سي', 'مكملات الحديد', 'موبيروسين', 'موكسيفلوكساسين', 'مونتيلوكاست', 'ميبيندازول', 'ميترونيدازول', 'ميتوكلوبراميد', 'ميمانتين', 'ناتاميسين', 'نياسيناميد', 'نيبافيناك', 'نيستاتين', 'هيالورونات الصوديوم', 'هيدروكسيزين', 'هيدروكورتيزون', 'هيدروكينون']

ArabicWords=['٨', 'دقائق', '١٢', 'قبل', 'الأكل', 'أسبوع', '٥', 'النوم', 'ليلا', 'ساعات', 'لأول', 'يوم', 'مرة', 'اليقظة', '٤', 'كل', '٧', 'دقيقة', 'أثناء', '٣', '٦', 'يومين', 'الفطار', 'مرتين', '١٤', 'واحدة', 'أيام', 'الغداء', 'اللزوم', 'ساعة', 'لمدة', 'يوميا', 'بعد', 'فقط', 'صباحا', 'عند', '١٥' ,'أتروبين', 'أزيثروميسين', 'أسيتات البريدنيزولون', 'أسيتازولاميد', 'أسيتيل سيستين', 'ألبيندازول', 'أمانتادين', 'أملاح الإماهة الفموية', 'أموكسيسيلين', 'أوفلوكساسين', 'أوميبرازول', 'أوندانسيترون', 'إريثرومايسين', 'إيبوبروفين', 'الببتيدات', 'البروبيوتيك', 'البوتوكس', 'الفيتامينات المتعددة', 'باراسيتامول', 'براميبيكسول', 'بريجابالين', 'بريدنيزولون', 'بريمونيدين', 'بيلوكاربين', 'بيماتوبروست', 'ترافوبروست', 'تروبيكاميد', 'تريتينوين', 'توبراميسين', 'توبيراميت', 'تيمولول', 'جابابنتين', 'جاتيفلوكساسين', 'حمض الجليكوليك', 'حمض الساليسيليك', 'حمض اللاكتيك', 'حمض الهيالورونيك', 'دموع صناعية', 'دورزولاميد', 'دوكسيسيكلين', 'دومبيريدون', 'دونيبيزيل', 'ديكساميثازون', 'ديكستروميثورفان', 'ديكلوفيناك', 'رانيتيدين', 'روبينيرول', 'ريتينول', 'ريفاستجمين', 'سالبيوتامول', 'سيبروفلوكساسين', 'سيتريزين', 'سيفدينير', 'سيفوريوكسيم', 'سيفيكسيم', 'سيكلوسبورين', 'غوايفينيسين', 'فالبروات', 'فلوروميثولون', 'فوريكونازول', 'فيتامين د', 'قطرات بريدنيزولون', 'كارباشول', 'كاربامازيبين', 'كاربوسيستين', 'كبريتات الزنك', 'كربونات الكالسيوم', 'كلورامفينيكول', 'كلورهيكسيدين', 'كليندامايسين', 'كولاجين', 'كيتورولاك', 'لاتانوبروست', 'لوراتادين', 'ليدوكايين', 'ليفوفلوكساسين', 'ليفيتيجراست', 'ليفيتيراسيتام', 'مانيتول', 'مصل فيتامين سي', 'مكملات الحديد', 'موبيروسين', 'موكسيفلوكساسين', 'مونتيلوكاست', 'ميبيندازول', 'ميترونيدازول', 'ميتوكلوبراميد', 'ميمانتين', 'ناتاميسين', 'نياسيناميد', 'نيبافيناك', 'نيستاتين', 'هيالورونات الصوديوم', 'هيدروكسيزين', 'هيدروكورتيزون', 'هيدروكينون']
EnglishWords=['Acetazolamide', 'Acetylcysteine', 'Albendazole', 'Amantadine', 'Amoxicillin', 'Artificial Tears', 'Atropine', 'Azithromycin', 'Bimatoprost', 'Botox', 'Brimonidine', 'Calcium Carbonate', 'Carbachol', 'Carbamazepine', 'Carbocisteine', 'Cefdinir', 'Cefixime', 'Cefuroxime', 'Cetirizine', 'Chloramphenicol', 'Chlorhexidine', 'Ciprofloxacin', 'Clindamycin', 'Collagen', 'Cyclosporine', 'Dexamethasone', 'Dextromethorphan', 'Diclofenac', 'Domperidone', 'Donepezil', 'Dorzolamide', 'Doxycycline', 'Erythromycin', 'Fluorometholone', 'Gabapentin', 'Gatifloxacin', 'Glycolic Acid', 'Guaifenesin', 'Hyaluronic Acid', 'Hydrocortisone', 'Hydroquinone', 'Hydroxyzine', 'Ibuprofen', 'Iron Supplements', 'Ketorolac', 'Lactic Acid', 'Latanoprost', 'Levetiracetam', 'Levofloxacin', 'Lidocaine', 'Lifitegrast', 'Loratadine', 'Mannitol', 'Mebendazole', 'Memantine', 'Metoclopramide', 'Metronidazole', 'Montelukast', 'Moxifloxacin', 'Multivitamins', 'Mupirocin', 'Natamycin', 'Nepafenac', 'Niacinamide', 'Nystatin', 'Ofloxacin', 'Omeprazole', 'Ondansetron', 'Oral Rehydration Salts', 'Paracetamol', 'Peptides', 'Pilocarpine', 'Pramipexole', 'Prednisolone', 'Prednisolone Acetate', 'Prednisolone Drops', 'Pregabalin', 'Probiotics', 'Ranitidine', 'Retinol', 'Rivastigmine', 'Ropinirole', 'Salbutamol', 'Salicylic Acid', 'Sodium Hyaluronate', 'Timolol', 'Tobramycin', 'Topiramate', 'Travoprost', 'Tretinoin', 'Tropicamide', 'Valproate', 'Vitamin C Serum', 'Vitamin D', 'Voriconazole', 'Zinc Sulfate''for', 'Every', 'After', 'Twice', 'needed', 'first', 'hours', 'breakfast', 'For', '8', 'awake', 'other', 'Night', 'hour', 'Morning', 'bed', '14', 'the', 'days', 'As', '5', 'bedtime', 'lunch', 'week', '7', 'daily', 'only', '4', 'Before', 'while', '3', 'minutes', '2', '6', 'day', '15', 'meals', 'Once', '12']

frequency_patterns = [
    ## 🔹 English Frequencies
    r"\bevery\s\d+\shours?\b",            # "every 6 hours"
    r"\bEvery\shours\b",
    r"\bevery\s\d+\s?-\s?\d+\shours?\b",  # "every 4-6 hours"
    r"\bonce\sdaily\b",                   # "once daily"
    r"\btwice\sdaily\b",                  # "twice daily"
    r"\bthree\stimes\sa\sday\b",          # "three times a day"
    r"\bfour\stimes\sa\sday\b",           # "four times a day"
    r"\b\d+\stimes\sa\sday\b",            # "5 times a day"

    ## ⏳ Time-Based
    r"\bevery\sother\sday\b",             # "every other day"
    r"\bevery\s\d+\sdays?\b",             # "every 3 days"
    r"\bevery\s\d+\sweeks?\b",            # "every 2 weeks"
    r"\bevery\s\d+\smonths?\b",           # "every 6 months"

    ## 🌙 Morning/Evening
    r"\bin\sthe\smorning\b",              # "in the morning"
    r"\bin\sthe\sevening\b",              # "in the evening"
    r"\bin\sthe\safternoon\b",            # "in the afternoon"
    r"\bin\sthe\snight\b",                # "in the night"
    r"\bdaily\sat\snoon\b",               # "daily at noon"

    ## 🍽 Meal-Based
    r"\bbefore\smeals?\b",                # "before meals"
    r"\bbefore\sbreakfast?\b",            # "before breakfast"
    r"\bafter\smeals?\b",                 # "after meals"
    r"\bafter\sbreakfast?\b",             # "after breakfast"
    r"\bbefore\sfood\b",                  # "before food"
    r"\bafter\sfood\b",                   # "after food"
    r"\bon\san\sempty\sstomach\b",        # "on an empty stomach"

    ## 🌙 Sleep
    r"\bbefore\sbedtime\b",               # "before bedtime"
    r"\bat\sbedtime\b",                   # "at bedtime"
    r"\bbefore\sgoing\sto\sbed\b",        # "before going to bed"

    ## 🔄 PRN (As Needed)
    r"\bas\sneeded\b",                    # "as needed"
    r"\bif\sneeded\b",                    # "if needed"
    r"\bwhen\snecessary\b",               # "when necessary"
    r"\bwhen\srequired\b",                # "when required"
    r"\bwhen\sfeeling\spain\b",           # "when feeling pain"

    ## 🚑 Perioperative
    r"\bbefore\ssurgery\b",               # "before surgery"
    r"\bafter\ssurgery\b",                # "after surgery"
    r"\bbefore\san\soperation\b",         # "before an operation"
    r"\bafter\san\soperation\b",          # "after an operation"

    ## 🔹 Arabic Frequencies
    r"\bكل\s\d+\sساعة\b",              # "كل 8 ساعات" (every X hours)
    r"\bكل\s\d+\s?-\s?\d+\sساعات?\b",  # "كل 4-6 ساعات" (every X-Y hours)
    r"\bمرة\sيوميا\b",                 # "مرة يوميًا" (once daily)
    r"\bمرة\sكل\sيوم\b",               # "مرة كل يوم" (once per day)
    r"\bمرة\sيوميا\b",                 # "مرة يوميا" (once per day)
    r"\bمرة\sأسبوعيا\b",               # "مرة أسبوعيًا" (once weekly)
    r"\bمرة\sكل\sأسبوع\b",             # "مرة كل أسبوع" (once per week)
    r"\bمرة\sشهريا\b",                 # "مرة شهريًا" (once monthly)
    r"\bمرة\sكل\sشهر\b",               # "مرة كل شهر" (once per month)
    r"\bمرتين\sيوميا\b",               # "مرتين يوميًا" (twice daily)
    r"\b\d+\sمرات?\sيوميا\b",          # "3 مرات يوميًا" (multiple times daily)

    ## ⏳ Time-Based
    r"\bكل\sيومين\b",                   # "كل يومين" (every other day)
    r"\bكل\s\d+\sأيام\b",               # "كل 3 أيام" (every X days)
    r"\bكل\s\d+\sأسابيع\b",             # "كل 2 أسابيع" (every X weeks)
    r"\bكل\s\d+\sشهور\b",               # "كل 6 شهور" (every X months)

   ## Arabic (Word-Based Numbers)
    r"\bكل\sساعة\b",                     # "كل واحدة ساعة" (every one hour)
    r"\bكل\sساعتين\b",                   # "كل اثنتين ساعة" (every two hours)
    r"\bكل\sثلاث\sساعات\b",               # "كل ثلاث ساعات" (every three hours)
    r"\bكل\sأربع\sساعات\b",              # "كل أربع ساعات" (every four hours)
    r"\bكل\sخمس\sساعات\b",               # "كل خمس ساعات" (every five hours)
    r"\bكل\sست\sساعات\b",                # "كل ست ساعات" (every six hours)
    r"\bكل\sسبع\sساعات\b",               # "كل سبع ساعات" (every seven hours)
    r"\bكل\sثماني\sساعات\b",             # "كل ثماني ساعات" (every eight hours)
    r"\bكل\sتسع\sساعات\b",               # "كل تسع ساعات" (every nine hours)
    r"\bكل\sعشر\sساعات\b",               # "كل عشر ساعات" (every ten hours)
    r"\bكل\sإحدى\sعشرة\sساعة\b",         # "كل إحدى عشرة ساعة" (every 11 hours)
    r"\bكل\sاثنتي\sعشرة\sساعة\b",        # "كل اثنتي عشرة ساعة" (every 12 hours)

    ## 🌙 Morning/Evening
    r"\bفي\sالصباح\b",                  # "في الصباح" (in the morning)
    r"\bفي\sالمساء\b",                  # "في المساء" (in the evening)
    r"\bفي\sالظهيرة\b",                 # "في الظهيرة" (at noon)
    r"\bفي\sالليل\b",                   # "في الليل" (at night)

    ## 🍽 Meal-Based
    r"\bقبل\sالأكل\b",                  # "قبل الأكل" (before meals)
    r"\bبعد\sالأكل\b",                  # "بعد الأكل" (after meals)
    r"\bقبل\sالطعام\b",                 # "قبل الطعام" (before food)
    r"\bبعد\sالطعام\b",                 # "بعد الطعام" (after food)
    r"\bعلى\sمعدة\sفارغة\b",            # "على معدة فارغة" (on an empty stomach)
    r"\bعلى\sالريق\b",                   # "على الريق" (fasting)

    ## 🌙 Sleep
    r"\bقبل\sالنوم\b",                 # "قبل النوم" (before sleep)
    r"\bعند\sالنوم\b",                 # "عند النوم" (at bedtime)

    ## 🔄 PRN (As Needed)
    r"\bعند\sاللزوم\b",                # "عند اللزوم" (as needed)
    r"\bحسب\sالحاجة\b",                # "حسب الحاجة" (as required)
    r"\bإذا\sاستدعت\sالحاجة\b",         # "إذا استدعت الحاجة" (if necessary)
    r"\bعند\sالشعور\sبالألم\b",          # "عند الشعور بالألم" (when feeling pain)

    ## 🚑 Perioperative
    r"\bقبل\sالعملية\b",              # "قبل العملية" (before surgery)
    r"\bبعد\sالعملية\b",              # "بعد العملية" (after surgery)
    r"\bقبل\sالتدخل\sالجراحي\b",     # "قبل التدخل الجراحي" (before an operation)
    r"\bبعد\sالتدخل\sالجراحي\b",     # "بعد التدخل الجراحي" (after an operation)
    r"\bEvery\s\d+\shours?\b",            # "Every 8 hours" (capitalized)
    r"\bEvery\shours?\b",                 # "Every hours" (capitalized)
    r"\bAfter\slunch\b",                  # "After lunch" (capitalized)
    r"\bOnce\sdaily\b",                   # "Once daily" (capitalized)

]

"""# **TR OCR MODEL**

## **load model with weights**
"""

# from google.colab import drive
# drive.mount('/content/drive')
# import zipfile
# import gdown

# # Download the zip file from Google Drive
# zip_path = 'https://drive.google.com/uc?id=1lzbd9t9aJ-NJYCS__8uzCpObjbsN5Tm2&export=download'  # Corrected URL for downloading
# output_path = '/content/model.zip'  # Path to save the downloaded zip file
# gdown.download(zip_path, output_path, quiet=False)

# extract_path = '/content/model_dir'

# # Open and extract the downloaded zip file
# with zipfile.ZipFile(output_path, 'r') as zip_ref: # Changed to use downloaded zip file path
#     zip_ref.extractall(extract_path)

from transformers import VisionEncoderDecoderModel, TrOCRProcessor
import torch
import os

MODEL_NAME = "microsoft/trocr-base-handwritten"
processor = TrOCRProcessor.from_pretrained(MODEL_NAME) # Initialize the processor here
new_model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)
new_model.config.decoder_start_token_id = processor.tokenizer.cls_token_id
new_model.config.pad_token_id = processor.tokenizer.pad_token_id
new_model.load_state_dict(torch.load("/kaggle/input/trocr_finetune_weights_stp/pytorch/default/1/model_weights.pth"))
print("Model weights loaded successfully into a new model.")

"""# **Define Functions**

## **vision functions**
"""

from sklearn.cluster import DBSCAN
def fuzzy_match(word, word_list, threshold=30):
    result = process.extractOne(word, word_list, scorer=fuzz.ratio)
    if result:
        # Handle different versions of fuzzywuzzy
        if isinstance(result, tuple) and len(result) >= 2:
            match, score = result[0], result[1]  # Extract match and score
            return match if score >= threshold else None
    return None

def remove_duplicate_boxes(boxes, iou_threshold=0.8):
    if len(boxes) == 0:
        return []

    # Convert boxes to (x1, y1, x2, y2) format
    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    # Compute the area of the bounding boxes
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Sort the boxes by the bottom-right y-coordinate
    indices = np.argsort(y2)
    keep = []

    while len(indices) > 0:
        last = len(indices) - 1
        i = indices[last]
        keep.append(i)

        # Compute the IoU of the remaining boxes with the last box
        xx1 = np.maximum(x1[i], x1[indices[:last]])
        yy1 = np.maximum(y1[i], y1[indices[:last]])
        xx2 = np.minimum(x2[i], x2[indices[:last]])
        yy2 = np.minimum(y2[i], y2[indices[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / areas[indices[:last]]

        # Remove boxes with IoU greater than the threshold
        indices = np.delete(indices, np.concatenate(([last], np.where(overlap > iou_threshold)[0])))

    return boxes[keep].tolist()

def sort_boxes_top_to_bottom_left_to_right(boxes):
    if len(boxes) == 0:
        return []

    # Convert boxes to numpy array
    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]

    # Sort the boxes by the top-left y-coordinate (y1), then by the top-left x-coordinate (x1)
    indices = np.lexsort((x1, y1))  # Sort by y1 first, then by x1
    return boxes[indices].tolist()

def preprocess_image(image):
        # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 20)
        kernel = np.ones((2, 2), np.uint8)
        img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
        img_clahe = clahe.apply(img_morph)
        return img_clahe

# -----------------------------------
def group_boxes_into_lines_and_sort(boxes, texts, vertical_threshold=20):
    if not boxes or not texts:
        return [], []

    # Convert boxes to include center points and other useful metrics
    box_data = []
    for i, (box, text) in enumerate(zip(boxes, texts)):
        if text:  # Only process boxes with valid text
            x1, y1, x2, y2 = box
            center_y = (y1 + y2) / 2
            center_x = (x1 + x2) / 2
            height = y2 - y1
            box_data.append({
                'index': i,
                'box': box,
                'text': text,
                'center_x': center_x,
                'center_y': center_y,
                'height': height
            })

    if not box_data:
        return [], []

    # Dynamically adjust vertical threshold based on average text height
    avg_height = sum(item['height'] for item in box_data) / len(box_data)
    dynamic_threshold = max(vertical_threshold, avg_height * 0.7)

    # Initial sort by y-coordinate
    box_data.sort(key=lambda x: x['center_y'])

    # Use DBSCAN clustering to group lines
    points = np.array([[item['center_x'], item['center_y']] for item in box_data])
    # Adjust eps based on average height
    clustering = DBSCAN(eps=dynamic_threshold, min_samples=1).fit(points)
    labels = clustering.labels_

    # Group boxes by cluster label
    lines = {}
    for i, label in enumerate(labels):
        if label not in lines:
            lines[label] = []
        lines[label].append(box_data[i])

    # Sort lines by average y-coordinate
    sorted_lines = sorted(lines.values(), key=lambda line: sum(item['center_y'] for item in line)/len(line))

    # Sort each line by x-coordinate (left to right)
    for line in sorted_lines:
        line.sort(key=lambda x: x['center_x'])

    # Extract the ordered text and boxes
    ordered_text = []
    ordered_boxes = []
    for line in sorted_lines:
        for box in line:
            ordered_text.append(box['text'])
            ordered_boxes.append(box['box'])

    return ordered_text, ordered_boxes

"""## **Text Extraction Function**"""

from PIL import Image
import cv2
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

def TextExtraction(images):
    extracted_data = []  # List to store results per input image

    for image_path in images:
        # Load image
        image = cv2.imread(image_path)
        image_data = {
            "image_path": image_path,
            "words": []  # List to store {text, position} for each word
        }

        # Run YOLOv8 detection
        results = model(image)
        boxes = results[0].boxes.xyxy.cpu().numpy()  # Bounding boxes
        class_ids = results[0].boxes.cls.cpu().numpy()  # Class IDs (0=Arabic, 1=English)

        # Remove duplicate boxes and sort
        boxes = remove_duplicate_boxes(boxes)
        sorted_boxes = sort_boxes_top_to_bottom_left_to_right(boxes)

        for i, box in enumerate(sorted_boxes):
            x1, y1, x2, y2 = map(int, box)
            cropped_image = image[y1:y2, x1:x2]

            # Preprocess for TrOCR
            trocr_input = preprocess_for_trocr(cropped_image)
            inputs = processor(images=trocr_input, return_tensors="pt").to(new_model.device)

            # Extract text
            with torch.no_grad():
                generated_ids = new_model.generate(**inputs)
                output_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

            # Fuzzy match with language-specific dictionary
            class_id = int(class_ids[i])
            word_list = ArabicWords if class_id == 0 else EnglishWords
            matched_text = fuzzy_match(output_text.strip(), word_list)

            # Save text + coordinates
            image_data["words"].append({
                "text": matched_text,
                "position": (x1, y1, x2, y2)  # (left, top, right, bottom)
            })

        extracted_data.append(image_data)

    return extracted_data

def TextExtraction(images):
    extracted_data = []
    for image_path in images:
        image = cv2.imread(image_path)
        image_data = {
            "image_path": image_path,
            "text": "",  # Full text in reading order
            "words": []  # List to store {text, position} for each word
        }

        # Run YOLOv8 detection
        results = model(image)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        class_ids = results[0].boxes.cls.cpu().numpy()

        # Remove duplicate boxes
        boxes = remove_duplicate_boxes(boxes)

        # Extract text from each box
        all_texts = []
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            cropped_image = image[y1:y2, x1:x2]

            # Preprocess for TrOCR
            trocr_input = preprocess_for_trocr(cropped_image)
            inputs = processor(images=trocr_input, return_tensors="pt").to(new_model.device)

            # Extract text
            with torch.no_grad():
                generated_ids = new_model.generate(**inputs)
                output_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

            # Fuzzy match with language-specific dictionary
            class_id = int(class_ids[i])
            word_list = ArabicWords if class_id == 0 else EnglishWords
            matched_text = fuzzy_match(output_text.strip(), word_list)
            if matched_text:
                all_texts.append(matched_text)
                # Save the original box for later
                boxes[i] = box  # Ensure box is in the right format

        # Group into lines and sort in reading order
        ordered_texts, ordered_boxes = group_boxes_into_lines_and_sort(boxes, all_texts)

        # Build the complete text and word objects
        full_text = " ".join(ordered_texts)
        image_data["text"] = full_text

        for text, box in zip(ordered_texts, ordered_boxes):
            x1, y1, x2, y2 = map(int, box)
            image_data["words"].append({
                "text": text,
                "position": (x1, y1, x2, y2)
            })

        extracted_data.append(image_data)

    return extracted_data

import pandas as pd
df=pd.read_excel("/kaggle/input/merge-file/merge_file.xlsx")

df.head()

import pandas as pd
import re

def extract_arabic_english_words(df, column_name):
    arabic_words = set()
    english_words = set()

    for entry in df[column_name].dropna():
        # Normalize separators (Arabic comma and normal comma) and split
        parts = re.split(r'[،,]', str(entry))
        for phrase in parts:
            # Extract all words (Arabic + English/numbers)
            words = re.findall(r'\b[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FFa-zA-Z0-9]+\b', phrase)
            for word in words:
                word = word.strip()
                if not word:
                    continue
                # Check if word is Arabic
                if re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]', word):
                    arabic_words.add(word)
                else:
                    english_words.add(word)

    return list(arabic_words), list(english_words)

arabic_list, english_list = extract_arabic_english_words(df, 'Appointment')

print("Arabic Words:", arabic_list)
print("English Words:", english_list)

print(len(arabic_list))
print(len(english_list))

"""## **Phase 2 function**

-----------------------
"""

DEFAULT_FREQUENCY = "Every 6 hours"

def extract_medicine_and_frequency(sentence, medicine_list, frequency_patterns):
    extracted_medicines = []
    extracted_frequencies = []
    medicine_positions = {}
    frequency_positions = {}

    # Step 1: Extract medicines and their positions
    for med in medicine_list:
        match = re.search(rf"\b{re.escape(med)}\b", sentence)
        if match:
            extracted_medicines.append(med)
            medicine_positions[med] = match.start()

    # Step 2: Extract frequencies and their positions
    for pattern in frequency_patterns:
        pattern_re = re.compile(pattern)
        matches = pattern_re.finditer(sentence)
        for match in matches:
            extracted_frequencies.append(match.group())
            frequency_positions[match.group()] = match.start()

    # Step 3: Sort medicines and frequencies by their position
    sorted_medicines = sorted(medicine_positions.items(), key=lambda x: x[1])
    sorted_frequencies = sorted(frequency_positions.items(), key=lambda x: x[1])

    # Step 4: Pair medicines with frequencies
    extracted_results = []
    freq_index = 0
    last_known_frequency = None

    for i, (med, med_pos) in enumerate(sorted_medicines):
        extracted_frequency = "Unknown"
        next_med_pos = sorted_medicines[i + 1][1] if i + 1 < len(sorted_medicines) else len(sentence)

        # Check if there are words between this medicine and the next
        words_between = sentence[med_pos + len(med):next_med_pos].strip()
        if words_between and len(words_between.split()) <= 3:
            extracted_frequency = words_between
        else:
            # Try to match frequency after the medicine (if ordered correctly)
            while freq_index < len(sorted_frequencies):
                freq, freq_pos = sorted_frequencies[freq_index]
                if freq_pos > med_pos and freq_pos < next_med_pos:
                    extracted_frequency = freq
                    last_known_frequency = freq
                    freq_index += 1
                    break
                freq_index += 1

            # If no direct match, use last known frequency
            if extracted_frequency == "Unknown" and last_known_frequency:
                extracted_frequency = last_known_frequency

            # If still unknown, use default
            if extracted_frequency == "Unknown":
                extracted_frequency = DEFAULT_FREQUENCY

        extracted_results.append((med, extracted_frequency))

    return extracted_results

def sort_words_by_position(word_data):
    # Sort by y1 (top-to-bottom), then by x1 (left-to-right)
    return sorted(word_data, key=lambda x: (x["position"][1], x["position"][0]))

def print_sorted_words(sorted_words):
    print("Sorted Words (Top-to-Bottom, Left-to-Right):")
    for i, word in enumerate(sorted_words):
        print(f"{i+1}: '{word['text']}' at {word['position']}")

def pair_medicine_frequency(sorted_words):
    pairs = []
    i = 0
    n = len(sorted_words)

    while i < n:
        current = sorted_words[i]
        current_text = current['text']
        current_pos = current['position']

        # Check if current word is likely a medicine
        if is_medicine(current_text):
            medicine = current_text
            frequency_parts = []

            # Look ahead for frequency components
            j = i + 1
            while j < n:
                next_word = sorted_words[j]
                next_text = next_word['text']
                next_pos = next_word['position']

                # Check vertical alignment (same approximate line)
                if abs(next_pos[1] - current_pos[1]) > 50:  # Not on same line
                    break

                # Check if it's part of frequency
                if is_frequency(next_text):
                    frequency_parts.append(next_text)
                elif frequency_parts:  # Stop if we already have frequency parts
                    break

                j += 1

            if frequency_parts:
                frequency = ' '.join(frequency_parts)
                pairs.append((medicine, frequency))
                i = j  # Skip processed words
            else:
                i += 1
        else:
            i += 1

    return pairs

def is_medicine(text):
    """Check if text is likely a medicine name"""
    medicine_indicators = ['mg', 'ml', 'g', 'tablet', 'capsule', 'injection']
    return any(indicator in text.lower() for indicator in medicine_indicators)

def is_frequency(text):
    """Check if text is likely a frequency instruction"""
    frequency_terms = ['every', 'hours', 'daily', 'weekly', 'monthly',
                      'before', 'after', 'with', 'meal', 'meals',
                      'once', 'twice', 'thrice', 'morning', 'evening',
                      'night', 'bedtime', 'breakfast', 'lunch', 'dinner']
    return any(term in text.lower() for term in frequency_terms)

"""# **Submit Function**"""

def organize_medication_instructions(words_with_coords):
    # Step 1: Calculate the center y-coordinate for each word's bounding box
    words_with_y_center = []
    for word_dict in words_with_coords:
        word = word_dict['text']
        coords = word_dict['position']  # Assuming this is (x1, y1, x2, y2)
        x1, y1, x2, y2 = coords
        y_center = (y1 + y2) / 2
        x_center = (x1 + x2) / 2
        words_with_y_center.append((word, y_center, x_center, coords))

    # Step 2: Sort words by their y-coordinate (top to bottom)
    words_with_y_center.sort(key=lambda x: x[1])

    # Step 3: Group words that are likely on the same line
    # We'll consider words to be on the same line if their y-centers are within a threshold
    y_threshold = 100  # This can be adjusted based on your document's layout

    lines = []
    current_line = [words_with_y_center[0]]

    for i in range(1, len(words_with_y_center)):
        current_word = words_with_y_center[i]
        previous_word = words_with_y_center[i-1]

        # If this word is close in y-position to the previous word, add it to the current line
        if abs(current_word[1] - previous_word[1]) < y_threshold:
            current_line.append(current_word)
        # Otherwise, start a new line
        else:
            lines.append(current_line)
            current_line = [current_word]

    # Add the last line if it's not empty
    if current_line:
        lines.append(current_line)

    # Step 4: Sort words within each line by x-coordinate (left to right)
    for i in range(len(lines)):
        lines[i].sort(key=lambda x: x[2])  # Sort by x_center

    # Step 5: Join words in each line to form complete instructions
    instructions = []
    for line in lines:
        instruction = " ".join(word[0] for word in line)
        instructions.append(instruction)

    return instructions

def create_medication_frequency_pairs(organized_instructions):
    # Step 1: Concatenate all instructions into one line
    all_text = " ".join(organized_instructions)


    # Step 3: Extract medication-frequency pairs
    medication_pairs = []

    # Simple approach: Find a medication and assume text until the next medication is its frequency
    for i, med in enumerate(medicine_list):
        match = re.search(r'\b' + med + r'\b', all_text, re.IGNORECASE)
        if match:
            start_idx = match.start()

            # Find the next medication in the text after this one
            next_med_idx = float('inf')
            for other_med in medicine_list:
                if other_med != med:
                    other_match = re.search(r'\b' + other_med + r'\b', all_text[start_idx+len(med):], re.IGNORECASE)
                    if other_match:
                        if start_idx + len(med) + other_match.start() < next_med_idx:
                            next_med_idx = start_idx + len(med) + other_match.start()

            # Extract the frequency instruction
            if next_med_idx != float('inf'):
                frequency = all_text[start_idx+len(med):next_med_idx].strip()
            else:
                frequency = all_text[start_idx+len(med):].strip()

            medication_pairs.append((med, frequency))

    # Step 4: More sophisticated approach using patterns specific to medication instructions
    if not medication_pairs:
        # Pattern: Look for medication name followed by frequency info
        patterns = [
            # Medication followed by "Every X hours"
            (r'(\b\w+\b)\s+Every\s+(\d+)\s+hours', lambda m: (m.group(1), f"Every {m.group(2)} hours")),

            # Medication followed by "Once daily"
            (r'(\b\w+\b)\s+Once\s+daily', lambda m: (m.group(1), "Once daily")),

            # Medication followed by "After lunch"
            (r'(\b\w+\b)\s+After\s+lunch', lambda m: (m.group(1), "After lunch")),

            # More patterns can be added for different frequency formats
        ]

        for pattern, extract_func in patterns:
            for match in re.finditer(pattern, all_text, re.IGNORECASE):
                medication_pairs.append(extract_func(match))

    return medication_pairs


# medication_pairs = create_medication_frequency_pairs(organized_instructions)

# print("\nMedication-Frequency Pairs:")
# for med, freq in medication_pairs:
#     print(f"- {med}: {freq}")

def find_original_text(original_text, lowercase_match):
    pattern = re.compile(re.escape(lowercase_match), re.IGNORECASE)
    match = pattern.search(original_text)
    if match:
        return match.group(0)
    return lowercase_match

def extract_medication_frequency_pairs(text, medicine_list, frequency_patterns):
    """
    Extract medication and frequency pairs from text using predefined lists
    
    Args:
        text (str): Full text to extract from
        medicine_list (list): List of medicine names to look for
        frequency_patterns (list): List of frequency patterns to match
        
    Returns:
        list: Tuples of (medicine, frequency)
    """
    # Initialize results
    med_freq_pairs = []
    
    # Find all medicine names in the text
    found_medicines = []
    for med in medicine_list:
        matches = re.finditer(r'\b' + re.escape(med) + r'\b', text, re.IGNORECASE)
        for match in matches:
            found_medicines.append((med, match.start(), match.end()))
    
    # Sort medicines by their position in text
    found_medicines.sort(key=lambda x: x[1])
    
    # Find all frequency patterns
    found_frequencies = []
    for pattern in frequency_patterns:
        # Remove regex syntax if it's a regex pattern
        search_pattern = pattern
        if pattern.startswith(r'\b') and pattern.endswith(r'\b'):
            search_pattern = pattern[2:-2]
        
        # Try to find matches for this pattern
        try:
            for match in re.finditer(search_pattern, text, re.IGNORECASE):
                found_frequencies.append((match.group(), match.start(), match.end()))
        except re.error:
            # If pattern is invalid regex, try as literal text
            for match in re.finditer(re.escape(search_pattern), text, re.IGNORECASE):
                found_frequencies.append((match.group(), match.start(), match.end()))
    
    # Sort frequencies by position
    found_frequencies.sort(key=lambda x: x[1])
    
    # Match each medicine with appropriate frequency
    default_frequency = "Every 6 hours"  # Default if none found
    
    for i, (med, med_start, med_end) in enumerate(found_medicines):
        # Initialize with default
        closest_freq = default_frequency
        closest_dist = float('inf')
        
        # Find closest frequency that follows this medicine
        for freq, freq_start, freq_end in found_frequencies:
            if med_end < freq_start:  # Frequency appears after medicine
                distance = freq_start - med_end
                # If it's closer than current closest and before next medicine
                next_med_start = float('inf')
                if i + 1 < len(found_medicines):
                    next_med_start = found_medicines[i+1][1]
                
                if distance < closest_dist and freq_start < next_med_start:
                    closest_dist = distance
                    closest_freq = freq
        
        # Get original case for medication from text
        orig_med = find_original_text(text, med)
        
        # Add the pair (use original medication name from medicine_list if possible)
        med_freq_pairs.append((orig_med, closest_freq))
    
    return med_freq_pairs

def submit(images):
    results = []  # Stores the output for all prescriptions

    # Step 1: Extract text and positions from all images
    extracted_data = TextExtraction(images)

    for prescription_data in extracted_data:
        # Step 2: Sort words by position (top-to-bottom, left-to-right)
        sorted_words = sort_words_by_position(prescription_data["words"])

        # Optional: Print sorted words for debugging
        print(f"\nSorted words for {prescription_data['image_path']}:")
        print_sorted_words(sorted_words)
        
        # ----------------------------------------------
        print("-------------------------------------------------------------------------------")
        organized_instructions = organize_medication_instructions(sorted_words)

        print("Organized Medication Instructions:")
        for i, instruction in enumerate(organized_instructions, 1):
            print(f"{i}. {instruction}")
        print("-------------------------------------------------------------------------------")

        # Extract full text from organized instructions
        full_text = " ".join(organized_instructions)
        
        # Use the extract_medication_frequency_pairs function
        medication_pairs = extract_medication_frequency_pairs(full_text, medicine_list, frequency_patterns)

        print("\nMedication-Frequency Pairs:")
        for med, freq in medication_pairs:
            print(f"- {med}: {freq}")

        # Store results
        results.append({
            "image_path": prescription_data["image_path"],
            "prescription_pairs": medication_pairs
        })

    return results

# Example list of image file paths (update with actual paths)
images = ['/kaggle/input/machathon6-phase1-images/Dental_prescription_591.jpg', '/kaggle/input/machathon6-phase1-images/Neurology_prescription_131.jpg']

# Call the submit function
results = submit(images)

# Print the structured results
for i, result in enumerate(results):
    print(f"\nPrescription {i + 1} ({result['image_path']}):")
    if not result["prescription_pairs"]:
        print("  No medicine-frequency pairs found")
    else:
        for medicine, frequency in result["prescription_pairs"]:
            print(f"  Medicine: {medicine}, Frequency: {frequency}")

