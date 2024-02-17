from docscan.doc import scan


class DocumentScanner:
    def __init__(self):
        pass

    def process_image(self, input_file_path, output_file_path):
        # Open the input file in binary mode and read its contents
        with open(input_file_path, "rb") as file:
            image_data = file.read()

        # Process the image data with the 'scan' function
        processed_image_data = scan(image_data)

        # Write the processed image data to the output file
        with open(output_file_path, "wb") as out_file:
            out_file.write(processed_image_data)


# Usage example
if __name__ == "__main__":
    scanner = DocumentScanner()
    scanner.process_image("pageCheck.jpg", "out.png")
