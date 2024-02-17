import cv2
import time
import os
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import uiud

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


def capture_image(camera_id, img_name, warmup_time=2):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    time.sleep(warmup_time)  # Wait for camera to warm up
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(img_name, frame)
        print(f"Image saved as {img_name}")
        upload_to_supabase(img_name)
    else:
        print("Can't receive frame (stream end?). Exiting ...")
    cap.release()


def upload_to_supabase(img_name):
    try:
        # Step 1: Upload the image to Supabase Storage
        with open(img_name, "rb") as img_file:
            # file_content = img_file.read()
            try:
                supabase.storage.from_("images").upload(path=img_name, file=img_file, file_options={'content_type': 'image/jpeg'})
            except Exception as e:
                print(f"Storage upload error occurred 😭: {e}")


        # Step 2: Construct the URL for the uploaded image
        # Note: Adjust the URL pattern if needed based on your Supabase setup
        image_url = f"{url}/storage/v1/object/public/images/{img_name}"

        # Step 3: Insert the image metadata and URL into the Supabase table
        timestamp = datetime.now().isoformat()  # Current timestamp as a string
        data = {"image_name": img_name, "timestamp": timestamp, "image_url": image_url}
        db_response = supabase.table("images").insert(data).execute()

        print(f"db_response: {db_response}")
        # if db_response.error:
        #     print(f"Failed to upload metadata to Supabase: {db_response}")
        # else:
        #     print("Image and metadata uploaded to Supabase successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    print("Finding available cameras...")
    cameras = list_cameras()
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
            img_name = f"page_{curr_page}-{curr_page+1}.jpg"
            curr_page += 2
            capture_image(camera_id, img_name)
            time.sleep(3)  # Subtract warmup time from the delay
    except KeyboardInterrupt:
        print("Program exited by user.")


if __name__ == "__main__":
    main()
