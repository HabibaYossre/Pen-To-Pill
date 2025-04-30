def remove_duplicate_boxes(boxes, iou_threshold=0.8):
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    indices = np.argsort(y2)
    keep = []
    while len(indices) > 0:
        last = len(indices) - 1
        i = indices[last]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[indices[:last]])
        yy1 = np.maximum(y1[i], y1[indices[:last]])
        xx2 = np.minimum(x2[i], x2[indices[:last]])
        yy2 = np.minimum(y2[i], y2[indices[:last]])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / areas[indices[:last]]
        indices = np.delete(indices, np.concatenate(([last], np.where(overlap > iou_threshold)[0])))
    return boxes[keep].tolist()

def sort_boxes_top_to_bottom_left_to_right(boxes):
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    indices = np.lexsort((x1, y1))
    return boxes[indices].tolist()

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 20)
    kernel = np.ones((2, 2), np.uint8)
    img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_morph)
    return img_clahe

def preprocess_for_trocr(cropped_image):
    rgb_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    image = pil_image.convert('L')
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    fixed_height = 64
    width_percent = (fixed_height / float(image.size[1]))
    new_width = int((float(image.size[0]) * float(width_percent)))
    image = image.resize((new_width, fixed_height), Image.Resampling.LANCZOS)
    image = image.convert('RGB')
    return image

def correct_text_with_bart(texts, tokenizer, model, device):
    corrected_texts = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True).to(device)
        with torch.no_grad():
            summary_ids = model.generate(inputs['input_ids'], max_length=1024, num_beams=4, early_stopping=True)
        corrected_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        corrected_texts.append(corrected_text)
    return corrected_texts

def split_into_medicine_dosage_pairs(corrected_text):
    pairs = []
    items = [item.strip() for item in corrected_text.split(',') if item.strip()]
    for item in items:
        parts = item.strip().split(maxsplit=1)
        if len(parts) == 2:
            medicine, dosage = parts
            pairs.append((medicine, dosage))
        else:
            pairs.append((parts[0], ""))
    return pairs
