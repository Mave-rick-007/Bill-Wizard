import re
from paddleocr import PaddleOCR
import cv2
from totalAmount import totalAmount
import pandas as pd
from classifier.prediction import pred 


pattern = r"(?i)(invoice|bill|receipt)"
# item_pattern = r'(\d+)\.(\D)|(\D+)\s*\d+x\d+=([\d.]+)'
item_pattern = r'(\D+)\s*\d+x\d+=([\d.]+)'

enhancer = r'(\d+)(\d{2})'





# Initialize PaddleOCR (specify language)
ocr = PaddleOCR(use_angle_cls=True, lang='en', det= True , det_db_thresh=0.3, det_db_box_thresh=0.5)  # For English language

from PIL import Image

strings_set = set()
amount = 0

def isInvoice(image_path):

    
    image = cv2.imread(image_path)


    result = ocr.ocr(image, cls=True)

    extracted_text = ""
    for line in result:
      for word_info in line:
        extracted_text += word_info[1][0] + " "
        print(f"Detected text: {word_info[1][0]}")


    


    
    matches = re.findall(pattern, extracted_text)
    if matches:
        print("invoice detected")
        strings_set.add(extracted_text)
        amount = totalAmount(extracted_text)
        print("amount",amount)
        print(extracted_text)


    # items = re.findall(item_pattern, extracted_text)
 

    # Find all matches in the text
    # matches = re.findall(products, extracted_text)

    # Initialize a list to collect items and prices
    data = []


    products = r'(\d+)\.([A-Za-z\s]+)|(\D+)\s*\d+x\d+=([\d.]+)'

    

    # Find all matches in the text
    matches = re.findall(item_pattern, extracted_text)

    # Process and print results
    # for match in matches:
    #     if match[0] and match[1]:  # For the first regex (\d+)\.([A-Za-z\s]+)
    #         print(f"\n\n0: {match[0]} x 1: {match[1]}")
    #         data.append((match[0], match[1]))
    #     elif match[2] and match[3]:  # For the second regex (\D+)\s*\d+x\d+=([\d.]+)
    #         print(f"\n\n2: {match[2]} x 3: {match[3]}")
    #         data.append((match[2], match[3]))


    # Create a DataFrame from the collected data
    df = pd.DataFrame(matches, columns=['Title', 'Price'])

    print(df)

    try:
        categorised = pred(df)
        print(categorised)
        return categorised
    except:
        print("error in detection")
    
        


        


# isInvoice('D:\\billDetection\\demoPhotos\\invoice12.jpg')

