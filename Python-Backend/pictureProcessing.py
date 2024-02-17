from doc import scan
import logging
import pytesseract
from PIL import Image
import os

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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scanner = DocumentScanner()
    
    folder = "./Python-Backend"
    png_files = sorted(
        [f for f in os.listdir(folder) if f.endswith('.png')],
        key=lambda x: int(os.path.splitext(x)[0].split('_')[1])
    )
    print(png_files)
    input_images = [os.path.join(folder, f)for f in png_files]
    output_images = [f.replace('.png', '_scanned.png') for f in input_images]
    for input_image, output_img in zip(input_images, output_images):
        scanner.process_image(input_image, output_img)
        text = pytesseract.image_to_string(Image.open(output_img))
        print(text)