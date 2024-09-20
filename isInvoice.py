import re
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image

strings_set = set()






def isInvoice(image_path):

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)



    print(text)

    pattern = r"(?i)(invoice|bill)"
    matches = re.findall(pattern, text)
    if (matches and (text not in strings_set)):
        strings_set.add(text)
        return True
        
    else:
        return False


isInvoice('D:\\billDetection\\demoPhotos\\invoice8.jpg')

