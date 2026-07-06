import os
import sys

def check_deps():
    missing = []

    try:
        import cv2  # noqa: F401
    except ImportError:
        missing.append("opencv-python")

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("pillow")

    if missing:
        print("ERROR: Missing dependencies:")
        for m in missing:
            print(f"  - {m}")

        print("\nInstall them with:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

check_deps()

import cv2
from PIL import Image

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_gif(input_path: str, output_dir: str):
    img = Image.open(input_path)

    frame = 0

    try:
        while True:
            img.seek(frame)

            frame_path = os.path.join(output_dir, f"frame_{frame:02d}.png")
            img.convert("RGBA").save(frame_path)

            print(f"Saved {frame_path}")
            frame += 1

    except EOFError:
        pass

    print(f"\nDone. Extracted {frame} frames from GIF.")

def extract_video(input_path: str, output_dir: str):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        sys.exit(1)

    frame = 0

    while True:
        ret, img = cap.read()
        if not ret:
            break

        frame_path = os.path.join(output_dir, f"frame_{frame:02d}.png")
        cv2.imwrite(frame_path, img)

        print(f"Saved {frame_path}")
        frame += 1

    cap.release()

    print(f"\nDone. Extracted {frame} frames from video.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_frames.py <input.gif|video>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print("Error: file not found")
        sys.exit(1)

    output_dir = "assets"
    ensure_dir(output_dir)

    ext = os.path.splitext(input_path)[1].lower()

    if ext == ".gif":
        extract_gif(input_path, output_dir)
    else:
        extract_video(input_path, output_dir)

if __name__ == "__main__":
    main()