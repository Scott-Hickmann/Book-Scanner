from docscan.doc import scan
import logging


class DocumentScanner:
    def __init__(self):
        self.model_downloaded = False

    def process_image(self, input_file_path, output_file_path):
        # Inform the user if the model is potentially being downloaded
        if not self.model_downloaded:
            logging.info(
                "Processing the image for the first time might take longer due to model download."
            )

        # Open the input file in binary mode and read its contents
        with open(input_file_path, "rb") as file:
            image_data = file.read()

        # Process the image data with the 'scan' function
        processed_image_data = scan(image_data)

        # After the first successful scan, assume the model is downloaded
        self.model_downloaded = True

        # Write the processed image data to the output file
        with open(output_file_path, "wb") as out_file:
            out_file.write(processed_image_data)


# Usage example
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scanner = DocumentScanner()
    scanner.process_image("pageCheck.jpg", "out.png")
