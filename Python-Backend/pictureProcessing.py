from doc import scan
import logging
from PIL import Image
import os
from google.cloud import vision
from autocorrect import Speller
import cv2
import numpy as np
import openai
from openai import OpenAI

class DocumentScanner:
    def __init__(self):
        self.model_downloaded = False

    def process_image(self, input_file_path, output_file_path):
        with open(input_file_path, 'rb') as input_file:
            input_image = Image.open(input_file)
            if input_image.mode != 'RGB':
                input_image = input_image.convert('RGB')
            rotated_image = input_image.rotate(-90, expand=True)
            temp_image_path = input_file_path.replace('.png', '_temp.png')
            rotated_image.save(temp_image_path)
            with open(temp_image_path, 'rb') as temp_file:
                temp_image_bytes = temp_file.read()
            scanned_data = scan(temp_image_bytes)
        with open(output_file_path, 'wb') as output_file:
            output_file.write(scanned_data)
        os.remove(temp_image_path)
    
    def ocr_image(self, input_file_path, sharpen=False, spellcheck=True):
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
        resp =  client.text_detection(image=google_img)
        ocr_output = resp.text_annotations[0].description.replace('\n',' ')

        if spellcheck:
            ocr_output = self.spellcheck(ocr_output)
        
        return ocr_output
    
    def spellcheck(self, text):
        chat_history = [
            {
                "role": "system",
                "content": f"Instructions: Correct any spelling, grammatical, capitalization, or syntactical mistakes in the following text. Fix any clearly incorrect phrases if you are sure that the fix is warranted. If the text seems out of order, please reorder it to make it coherent."
            },
            {
                "role": "user",
                "content": "immediafly disagreed with my 9/26/15 A New Light! I Sister on which Journal to use. wanted to use this one, my sister wanted me to use a Circle du Silver I journal. We argued for a while. and I decided to use this journal. for the pen slot. Anyway, I have a newfound interest in making `rhymes` that are bad"
            },
            {
                "role": "assistant",
                "content": "9/26/15 I immediately disagreed with my sister on which journal to use. I wanted to use this one, my sister wanted me to use a Circle du Soleil journal. We argued for a while, and I decided to use this journal for the pen slot. Anyway, I have a newfound interest in making rhymes that are bad."
            }
        ]
        client = OpenAI(api_key='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')
        chat_history.append({"role": "user", "content": f"Text: {text}"})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
        )
        return response.choices[0].message.content
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scanner = DocumentScanner()
    
    folder = "./Python-Backend"
    # png_files = sorted(
    #     [f for f in os.listdir(folder) if f.endswith('.png')],
    #     key=lambda x: int(os.path.splitext(x)[0].split('_')[1])
    # )
    png_files = ["IMG_3008.png"]
    print(png_files)
    input_images = [os.path.join(folder, f)for f in png_files]
    output_images = [f.replace('.png', '_scanned.png') for f in input_images]
    whole_text = ""
    for input_img, output_img in zip(input_images, output_images):
        scanner.process_image(input_img, output_img)
        text = scanner.ocr_image(output_img)
        print(text)
        whole_text += text + "\n"