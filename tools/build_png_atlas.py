from PIL import Image
import os
import math
import json

# ---------------- CONFIG ----------------
INPUT_DIR = "assets"
OUTPUT_ATLAS = "assets/atlas.png"
OUTPUT_META = "assets/meta.json"

TARGET_HEIGHT = 480   # resize frames to this height (controls performance + size)
MAX_COLS = None       # set to int if you want fixed columns
# ----------------------------------------

files = sorted([
    f for f in os.listdir(INPUT_DIR)
    if f.startswith("frame_") and f.endswith(".png")
])

if not files:
    raise RuntimeError("No frames found in assets/")

imgs = []

for f in files:
    path = os.path.join(INPUT_DIR, f)
    img = Image.open(path).convert("RGBA")

    w, h = img.size
    scale = TARGET_HEIGHT / h
    new_size = (int(w * scale), TARGET_HEIGHT)

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
print(meta)