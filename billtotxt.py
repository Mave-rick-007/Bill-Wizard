import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image


def billtotxt(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

