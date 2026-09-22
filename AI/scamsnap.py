# backend/scamsnap.py
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        # Convert image to grayscale for cleaner string readings
        img = img.convert('L')
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        # Fallback if tesseract isn't fully initialized on system path
        return ""