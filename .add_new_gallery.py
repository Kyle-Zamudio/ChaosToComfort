"""Convert new HEIC photos to web-optimized JPGs in gallery/."""
import pillow_heif
pillow_heif.register_heif_opener()
from PIL import Image
from pathlib import Path

SRC = Path(r"C:\Users\zkyle\Documents\Chaos to Comfort\Before and After")
DST = Path(r"C:\Users\zkyle\Documents\Chaos to Comfort\gallery")
MAX_W = 1200
QUALITY = 82

NEW = [
    ("Room_1_before.heic", "11-room-before.jpg"),
    ("Room_1_after.heic", "11-room-after.jpg"),
    ("Stairs_1_before.heic", "12-stairs-before.jpg"),
    ("Stairs_1_after.heic", "12-stairs-after.jpg"),
    ("Garage_1_before.heic", "13-garage-before.jpg"),
    ("Garage_1_after.heic", "13-garage-after.jpg"),
]

# Renumber existing composites to free up 11-13 for new pairs
RENAMES = [
    ("11-window-composite.jpg", "21-window-composite.jpg"),
    ("12-closet-composite.jpg", "22-closet-composite.jpg"),
    ("13-kitchen-white-composite.jpg", "23-kitchen-white-composite.jpg"),
    ("14-craft-desk-composite.jpg", "24-craft-desk-composite.jpg"),
    ("15-playroom-composite.jpg", "25-playroom-composite.jpg"),
    ("16-toy-nook-composite.jpg", "26-toy-nook-composite.jpg"),
    ("17-bedroom-empty-composite.jpg", "27-bedroom-empty-composite.jpg"),
]

import shutil
for old, new in RENAMES:
    if (DST / old).exists() and not (DST / new).exists():
        (DST / old).rename(DST / new)
        print(f"renamed {old} -> {new}")

for src_name, dst_name in NEW:
    src = SRC / src_name
    dst = DST / dst_name
    if not src.exists():
        print(f"MISSING: {src_name}")
        continue
    img = Image.open(src)
    # Honor EXIF orientation (iPhone photos often need rotation)
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    if img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    if w > MAX_W:
        new_h = int(h * MAX_W / w)
        img = img.resize((MAX_W, new_h), Image.LANCZOS)
    img.save(dst, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print(f"{dst_name:36} {dst.stat().st_size//1024:>4} KB ({img.size[0]}x{img.size[1]})")
