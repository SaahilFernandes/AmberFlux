import cv2
import os


def extract_frames(video_path, interval=1, output_dir="extracted_frames"):
    os.makedirs(output_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    success, image = vidcap.read()
    count = 0
    saved_paths = []

    while success:
        if int(vidcap.get(1)) % (fps * interval) == 0:
            frame_path = f"{output_dir}/frame_{count}.jpg"
            cv2.imwrite(frame_path, image)
            saved_paths.append(frame_path)
            count += 1
        success, image = vidcap.read()

    vidcap.release()
    return saved_paths
