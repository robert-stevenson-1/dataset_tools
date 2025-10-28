import os
import cv2
import glob
from tqdm import tqdm

# ==== CONFIGURATION ====
DATA_ROOT = "/root/zfs-crow-compute/datasets/PCN/bottle-1/final_dataset"  # path to your dataset root
OUT_ROOT = "/root/zfs-crow-compute/datasets/PCN/bottle-1/final_dataset_tiled"  # output dataset root
TILE_SIZE = 1024  # tile width/height
OVERLAP = 0.2     # fraction (e.g., 0.2 = 20% overlap)
IMG_EXT = ".jpg"   # or ".png"

# ========================

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def clip_boxes(boxes, x0, y0, x1, y1, img_w, img_h):
    """Clip YOLO boxes (normalized) to the crop region."""
    new_boxes = []
    for b in boxes:
        cls, cx, cy, w, h = b
        abs_x = cx * img_w
        abs_y = cy * img_h
        abs_w = w * img_w
        abs_h = h * img_h
        x_min = abs_x - abs_w / 2
        y_min = abs_y - abs_h / 2
        x_max = abs_x + abs_w / 2
        y_max = abs_y + abs_h / 2
        # Skip boxes completely outside crop
        if x_max < x0 or x_min > x1 or y_max < y0 or y_min > y1:
            continue
        # Clip box to tile bounds
        new_xmin = max(x_min, x0)
        new_ymin = max(y_min, y0)
        new_xmax = min(x_max, x1)
        new_ymax = min(y_max, y1)
        new_w = new_xmax - new_xmin
        new_h = new_ymax - new_ymin
        if new_w <= 1 or new_h <= 1:
            continue
        new_cx = (new_xmin + new_xmax) / 2 - x0
        new_cy = (new_ymin + new_ymax) / 2 - y0
        new_boxes.append([
            int(cls),
            new_cx / (x1 - x0),
            new_cy / (y1 - y0),
            new_w / (x1 - x0),
            new_h / (y1 - y0)
        ])
    return new_boxes


def process_split(split):
    print(f"\n🔹 Processing {split} split...")

    # <-- FIXED: your dataset has images/train/, not train/images/
    img_dir = os.path.join(DATA_ROOT, "images", split)
    label_dir = os.path.join(DATA_ROOT, "labels", split)

    out_img_dir = os.path.join(OUT_ROOT, "images", split)
    out_label_dir = os.path.join(OUT_ROOT, "labels", split)
    ensure_dir(out_img_dir)
    ensure_dir(out_label_dir)

    img_paths = glob.glob(os.path.join(img_dir, f"*{IMG_EXT}"))
    print(f"Found {len(img_paths)} images in {img_dir}")

    for img_path in tqdm(img_paths):
        img = cv2.imread(img_path)
        if img is None:
            print(f"⚠️ Could not read {img_path}, skipping.")
            continue

        h, w = img.shape[:2]
        name = os.path.splitext(os.path.basename(img_path))[0]
        label_path = os.path.join(label_dir, f"{name}.txt")

        boxes = []
        if os.path.exists(label_path):
            with open(label_path) as f:
                for line in f:
                    vals = line.strip().split()
                    if len(vals) == 5:
                        boxes.append(list(map(float, vals)))

        step_x = int(TILE_SIZE * (1 - OVERLAP))
        step_y = int(TILE_SIZE * (1 - OVERLAP))

        for y0 in range(0, h, step_y):
            for x0 in range(0, w, step_x):
                x1 = min(x0 + TILE_SIZE, w)
                y1 = min(y0 + TILE_SIZE, h)
                crop = img[y0:y1, x0:x1]

                # 🧩 Pad to square if smaller on right/bottom edges
                pad_bottom = TILE_SIZE - crop.shape[0]
                pad_right = TILE_SIZE - crop.shape[1]
                if pad_bottom > 0 or pad_right > 0:
                    crop = cv2.copyMakeBorder(
                        crop,
                        0, pad_bottom, 0, pad_right,
                        borderType=cv2.BORDER_CONSTANT,
                        value=[0, 0, 0]  # black padding
                    )

                tile_name = f"{name}_{x0}_{y0}"
                out_img_path = os.path.join(out_img_dir, f"{tile_name}{IMG_EXT}")
                cv2.imwrite(out_img_path, crop)

                new_boxes = clip_boxes(boxes, x0, y0, x1, y1, w, h)
                if new_boxes:
                    out_label_path = os.path.join(out_label_dir, f"{tile_name}.txt")
                    with open(out_label_path, "w") as f:
                        for b in new_boxes:
                            f.write(" ".join(map(str, b)) + "\n")

if __name__ == "__main__":
    for split in ["train", "val", "test"]:
        process_split(split)

    print("\n✅ Done! Tiled dataset created at:", OUT_ROOT)
