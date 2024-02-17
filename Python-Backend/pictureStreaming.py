import cv2
import time
import os
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import uuid
from pypdf import PdfWriter, PdfReader
from PIL import Image
import img2pdf

from pictureProcessing import DocumentScanner

load_dotenv()
url="https://eswlryiffkybjojdjkbv.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzd2xyeWlmZmt5YmpvamRqa2J2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwODE1Mjc2MiwiZXhwIjoyMDIzNzI4NzYyfQ.dpyLWxhN9IbvijXrxxMKwlBve6wBoPB3noBh74SrO4s"
supabase: Client = create_client(url, key)


def list_cameras(max_checks=10):
    available_cameras = []
    for i in range(max_checks):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
        else:
            break  # Stop the loop if a camera index is not available
    return available_cameras


def add_to_pdf(img_name, session_uuid, pdf_writer):
    # Convert image to PDF
    with open(img_name, "rb") as img_file:
        img_pdf = img2pdf.convert(img_file)

    # Save the image PDF temporarily
    temp_img_pdf_name = f"./{session_uuid}/temp_img.pdf"
    with open(temp_img_pdf_name, "wb") as img_pdf_file:
        img_pdf_file.write(img_pdf)

    # Read the temporary image PDF and add its page to the main PDF
    temp_img_pdf = PdfReader(temp_img_pdf_name)
    pdf_writer.add_page(temp_img_pdf.pages[0])

    # Save the updated main PDF
    with open(f"./{session_uuid}/scan.pdf", "wb") as f:
        pdf_writer.write(f)

    # Remove the temporary image PDF
    os.remove(temp_img_pdf_name)

    # Upload the updated main PDF to Supabase
    upload_pdf_to_supabase(f"./{session_uuid}/scan.pdf", session_uuid)


def capture_image(camera_id, img_name, session_uuid, pdf_writer, warmup_time=2):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    time.sleep(warmup_time)  # Wait for camera to warm up
    ret, frame = cap.read()
    if ret:
        raw_img_name = img_name.replace(".jpg", "_raw.jpg")
        cv2.imwrite(raw_img_name, frame)
        print(f"Raw image saved as {raw_img_name}.")
        scanner = DocumentScanner()
        scanner.process_image(raw_img_name, img_name)
        print("Scan complete. Parsing text...")
        text = scanner.ocr_image(img_name)
        print("Done. uploading to Supabase.")
        upload_to_supabase(img_name, text, session_uuid)
        add_to_pdf(img_name, session_uuid, pdf_writer)
    else:
        print("Can't receive frame (stream end?). Exiting ...")
    cap.release()


# Upload images and text to supabase
def upload_to_supabase(img_name, text, session_uuid):
    try:
        image_url = f"{url}/storage/v1/object/public/images/{img_name}"
        timestamp = datetime.now().isoformat()  # Current timestamp as a string
        
        data = {
            "image_name": img_name,
            "timestamp": timestamp,
            "image_url": image_url,
            "doc_id": session_uuid,
            "text": text,
        }

        # Upsert the image metadata and URL into the Supabase table
        db_response = supabase.table("pages").upsert(data).execute()

    except Exception as e:
        print(f"An error occurred: {e}")


# Upload rolling pdf to supabase
def upload_pdf_to_supabase(pdf_name, session_uuid):
    try:
        # Step 1: Upload the image to Supabase Storage

        # Step 1a: Check if the pdf already exists in the storage
        existing_files = supabase.storage.from_("pdfs").list()
        if any(file["name"] == pdf_name for file in existing_files):
            # Delete the existing pdf
            supabase.storage.from_("pdfs").remove([pdf_name])
        with open(pdf_name, "rb") as pdf_file:
            try:
                supabase.storage.from_("pdfs").upload(
                    path=pdf_name,
                    file=pdf_file,
                    file_options={
                        "content_type": "application/pdf",
                    },
                )
            except Exception as e:
                print(f"Storage upload error occurred 😭: {e}")

        # Step 2: Construct the URL for the uploaded image
        # Note: Adjust the URL pattern if needed based on your Supabase setup
        pdf_url = f"{url}/storage/v1/object/public/pdfs/{pdf_name}"

        # Step 3: Insert the image metadata and URL into the Supabase table
        timestamp = datetime.now().isoformat()  # Current timestamp as a string
        data = {
            "pdf_name": pdf_name,
            "timestamp": timestamp,
            "pdf_url": pdf_url,
            "doc_id": session_uuid,
        }
        try:
            db_response = supabase.table("pdfs").upsert(data).execute()
        except Exception as e:
            print(f"PDF DB insert error occurred 😭: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
        

def main():
    print("Finding available cameras...")
    cameras = list_cameras()
    session_uuid = str(uuid.uuid4())
    print(f"Session UUID: {session_uuid}")

    pdf_writer = PdfWriter()

    if cameras:
        print("Available camera IDs:", cameras)
        camera_id = int(input("Enter camera ID: "))
        if camera_id not in cameras:
            print("Invalid camera ID selected. Exiting...")
            return
    else:
        print("No cameras found. Exiting...")
        return

    os.mkdir(session_uuid)
    curr_page = 1
    try:
        while True:
            img_name = f"./{session_uuid}/page_{curr_page}-{curr_page+1}.jpg"
            curr_page += 2
            capture_image(camera_id, img_name, session_uuid, pdf_writer)
            time.sleep(3)
    except KeyboardInterrupt:
        print("Program exited by user.")


if __name__ == "__main__":
    main()
