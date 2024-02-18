from doc import scan
# from docscan.doc import scan
from google.cloud import vision
import cv2
import numpy as np

class DocumentScanner:
    def __init__(self):
        self.model_downloaded = False

    def process_image(self, input_file_path, output_file_path):
        with open(input_file_path, 'rb') as input_file:
            input_image = input_file.read()
            scanned_data = scan(input_image)
        with open(output_file_path, 'wb') as output_file:
            output_file.write(scanned_data)
    
    def ocr_image(self, input_file_path, sharpen=False):
        img = cv2.imread(input_file_path)
        if sharpen:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            img = cv2.filter2D(img, -1, sharpen_kernel)
            img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        success, img_jpg = cv2.imencode('.jpg', img)
        byte_img = img_jpg.tobytes()
        google_img = vision.Image(content=byte_img)
        
        client = vision.ImageAnnotatorClient()
        resp = client.text_detection(image=google_img)
        if len(resp.text_annotations) == 0:
            return ""
        ocr_output = resp.text_annotations[0].description.replace('\n',' ')
        return ocr_output