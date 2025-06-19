import re
from PIL import Image
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

def extract_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'
    return text

def extract_from_scanned_pdf(path):
    text = ""
    pages = convert_from_path(path)
    for page in pages:
        image = page.convert('RGB')
        # Optional: image = preprocess_image(image)
        ocr = pytesseract.image_to_string(image)
        text += ocr + '\n'
    return text

def extract_from_image(path):
    try:
        image = Image.open(path).convert("RGB")
        # Optional: image = preprocess_image(image)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise RuntimeError(f"Image OCR failed: {str(e)}")

def extract_from_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# Optional image preprocessing
# def preprocess_image(image):
#     if isinstance(image, Image.Image):
#         image = np.array(image.convert('RGB'))
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (0, 0), 3)
#     sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
#     _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     return binary

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[[^\]]*\]', '', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()

def handle_file(path, type):
    if type == "pdf":
        text = extract_from_pdf(path)
    elif type == "scanned_pdf":
        text = extract_from_scanned_pdf(path)
    elif type == "image":
        text = extract_from_image(path)
    elif type == "txt":
        text = extract_from_txt(path)
    else:
        raise ValueError("Unsupported file type.")

    return preprocess_text(text)
