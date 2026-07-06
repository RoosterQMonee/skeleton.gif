import os
import sys
import math
import json

def check_deps():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("ERROR: Missing dependency: pillow")
        print("Install with:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

check_deps()

from PIL import Image

# ---------------- CONFIG ----------------
INPUT_DIR = "assets"
OUTPUT_ATLAS = "assets/atlas.png"
OUTPUT_META = "assets/meta.json"

TARGET_HEIGHT = 480
MAX_COLS = None
# ----------------------------------------

def main():
    if not os.path.isdir(INPUT_DIR):
        print(f"ERROR: Input directory not found: {INPUT_DIR}")
        sys.exit(1)

    files = sorted([
        f for f in os.listdir(INPUT_DIR)
        if f.startswith("frame_") and f.endswith(".png")
    ])

    if not files:
        print("ERROR: No frames found in assets/")
        sys.exit(1)

    imgs = []

    for f in files:
        path = os.path.join(INPUT_DIR, f)

        try:
            img = Image.open(path).convert("RGBA")
        except Exception as e:
            print(f"ERROR: Failed to load {path}: {e}")
            sys.exit(1)

        w, h = img.size
        scale = TARGET_HEIGHT / float(h)
        new_size = (max(1, int(w * scale)), TARGET_HEIGHT)

        img = img.resize(new_size, Image.Resampling.LANCZOS)
        imgs.append(img)

    frame_w, frame_h = imgs[0].size
    count = len(imgs)

    if MAX_COLS:
        cols = MAX_COLS
    else:
        cols = math.ceil(math.sqrt(count))

    rows = math.ceil(count / cols)

    atlas_w = cols * frame_w
    atlas_h = rows * frame_h

    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))

    for i, img in enumerate(imgs):
        x = (i % cols) * frame_w
        y = (i // cols) * frame_h
        atlas.paste(img, (x, y))

    os.makedirs(os.path.dirname(OUTPUT_ATLAS), exist_ok=True)

    atlas.save(
        OUTPUT_ATLAS,
        "PNG",
        optimize=True,
        compress_level=9
    )

    meta = {
        "frame_count": count,
        "cols": cols,
        "rows": rows,
        "frame_w": frame_w,
        "frame_h": frame_h,
        "atlas_w": atlas_w,
        "atlas_h": atlas_h
    }

    with open(OUTPUT_META, "w") as f:
        json.dump(meta, f, indent=2)

    print("Atlas generated:")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()