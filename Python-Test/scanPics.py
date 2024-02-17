import cv2
import time
import os
from supabase import create_client, Client

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
    else:
        print("Can't receive frame (stream end?). Exiting ...")
    cap.release()


def main():
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
            time.sleep(10 - 2)  # Subtract warmup time from the delay
    except KeyboardInterrupt:
        print("Program exited by user.")

if __name__ == "__main__":
    main()
