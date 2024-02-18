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
import threading
from openai import OpenAI
from controller import control

from pictureProcessing import DocumentScanner

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
    with open(img_name, "rb") as img_file:
        img_pdf = img2pdf.convert(img_file)
    temp_img_pdf_name = f"temp_img_{session_uuid}.pdf"
    with open(temp_img_pdf_name, "wb") as img_pdf_file:
        img_pdf_file.write(img_pdf)
    temp_img_pdf = PdfReader(temp_img_pdf_name)
    pdf_writer.add_page(temp_img_pdf.pages[0])
    with open(f"scan_{session_uuid}.pdf", "wb") as f:
        pdf_writer.write(f)
    os.remove(temp_img_pdf_name)
    upload_pdf_to_supabase(f"scan_{session_uuid}.pdf", session_uuid)

def spellcheck_and_upload_text(raw_text, img_name, session_uuid):
    print("Spellchecking text...")
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
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    chat_history.append({"role": "user", "content": f"Text: {raw_text}"})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )
    text = response.choices[0].message.content
    _upload_text_to_supabase(text, img_name, session_uuid)
    print("Text uploaded to Supabase.")

def capture_image(camera_id, img_name, session_uuid, pdf_writer, warmup_time=2, spellcheck=True):
    print("Capturing image...")
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    time.sleep(warmup_time)  # Wait for camera to warm up
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1) # Flip the image horizontally
        frame = cv2.flip(frame, 0) # Flip the image vertically
        raw_img_name = img_name.replace(".jpg", "_raw.jpg")
        cv2.imwrite(raw_img_name, frame)
        print(f"Raw image saved as {raw_img_name}.")
        scanner = DocumentScanner()
        scanner.process_image(raw_img_name, img_name)
        upload_img_to_supabase(img_name, session_uuid)
        print("Image uploaded to Supabase.")
        raw_text = scanner.ocr_image(img_name)
        if spellcheck:
            spellcheck_thread = threading.Thread(target=spellcheck_and_upload_text, args=(raw_text, img_name, session_uuid))
            spellcheck_thread.start()
        add_to_pdf(img_name, session_uuid, pdf_writer)
    else:
        print("Can't receive frame (stream end?). Exiting ...")
    cap.release()

def _upload_text_to_supabase(text, image_name, session_uuid):
    try:
        timestamp = datetime.now().isoformat()
        data = {
            "text": text,
            "timestamp": timestamp,
            "image_name": image_name,
            "doc_id": session_uuid,
        }
        db_response = supabase.table("texts").upsert(data).execute()
    except Exception as e:
        print(f"An error occurred: {e}")

def upload_img_to_supabase(img_name, session_uuid):
    with open(img_name, "rb") as img_file:
        supabase.storage.from_("images").upload(
            path=img_name,
            file=img_file,
            file_options={"content_type": "image/jpeg"},
        )
    
    try:
        image_url = f"{url}/storage/v1/object/public/images/{img_name}"
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
                        "content-type": "application/pdf",
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

    def on_scan_read():
        nonlocal curr_page
        img_name = f"page_{curr_page}-{curr_page+1}_{session_uuid}.jpg"
        curr_page += 2
        capture_image(camera_id, img_name, session_uuid, pdf_writer)
    
    control(on_scan_read)


if __name__ == "__main__":
    main()
