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


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
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
    temp_img_pdf_name = f"temp_img_{session_uuid}.pdf"
    with open(temp_img_pdf_name, "wb") as img_pdf_file:
        img_pdf_file.write(img_pdf)

    # Read the temporary image PDF and add its page to the main PDF
    temp_img_pdf = PdfReader(temp_img_pdf_name)
    pdf_writer.add_page(temp_img_pdf.pages[0])

    # Save the updated main PDF
    with open(f"scan_{session_uuid}.pdf", "wb") as f:
        pdf_writer.write(f)

    # Remove the temporary image PDF
    os.remove(temp_img_pdf_name)

    # Upload the updated main PDF to Supabase
    upload_pdf_to_supabase(f"scan_{session_uuid}.pdf", session_uuid)


def capture_image(camera_id, img_name, session_uuid, pdf_writer, warmup_time=2):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    time.sleep(warmup_time)  # Wait for camera to warm up
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(img_name, frame)
        print(f"Image saved as {img_name}")
        upload_to_supabase(img_name, session_uuid)
        add_to_pdf(img_name, session_uuid, pdf_writer)
    else:
        print("Can't receive frame (stream end?). Exiting ...")
    cap.release()


# Upload images to supabase
def upload_to_supabase(img_name, session_uuid):
    try:
        # Check if the image already exists in the storage
        existing_files = supabase.storage.from_("images").list()
        if any(file["name"] == img_name for file in existing_files):
            # Delete the existing image
            supabase.storage.from_("images").remove([img_name])

        # Upload the new image to Supabase Storage
        with open(img_name, "rb") as img_file:
            supabase.storage.from_("images").upload(
                path=img_name,
                file=img_file,
                file_options={"content_type": "image/jpeg"},
            )

        # Construct the URL for the uploaded image
        image_url = f"{url}/storage/v1/object/public/images/{img_name}"

        # Prepare the data for upsert operation
        timestamp = datetime.now().isoformat()  # Current timestamp as a string
        data = {
            "image_name": img_name,
            "timestamp": timestamp,
            "image_url": image_url,
            "doc_id": session_uuid,
        }

        # Upsert the image metadata and URL into the Supabase table
        db_response = supabase.table("images").upsert(data).execute()

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
    curr_page = 1
    try:
        while True:
            img_name = f"page_{curr_page}-{curr_page+1}_{session_uuid}.jpg"
            curr_page += 2
            capture_image(camera_id, img_name, session_uuid, pdf_writer)
            time.sleep(3)
    except KeyboardInterrupt:
        print("Program exited by user.")


if __name__ == "__main__":
    main()
