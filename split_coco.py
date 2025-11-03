import json
import random
import os
from pathlib import Path

# --- Configuration ---

# 1. Set the path to the directory containing your annotations
data_root = "/root/zfs-crow-compute/datasets/PCN/all-bottles/PCN_Dish_B1+2_COCO" 

# 2. Set the name of your single, combined COCO file
original_json_name = "result.json" # This is the default from Label Studio

# 3. Set the desired names for your new split files
train_json_name = "train.json"
val_json_name = "val.json"

# 4. Set your desired training/validation split ratio (e.g., 0.8 = 80% train, 20% val)
split_ratio = 0.8

# 5. Set the images directory relative to data_root
images_dir_name = "images"

# --- End Configuration ---

# Construct full paths
original_json_path = os.path.join(data_root, original_json_name)
train_json_path = os.path.join(data_root, train_json_name)
val_json_path = os.path.join(data_root, val_json_name)
images_dir = os.path.join(data_root, images_dir_name)

print(f"Loading original annotations from: {original_json_path}")

# Load the original COCO JSON
with open(original_json_path, 'r') as f:
    coco_data = json.load(f)

# Get list of actual images in the directory
print(f"Checking images directory: {images_dir}")
if os.path.exists(images_dir):
    actual_image_files = set(os.listdir(images_dir))
    print(f"Found {len(actual_image_files)} image files in directory")
else:
    print(f"WARNING: Images directory not found: {images_dir}")
    actual_image_files = set()

# Fix image paths and filter out missing images
print("Fixing image paths...")
valid_images = []
missing_images = []

for img in coco_data['images']:
    old_path = img['file_name']
    # Extract just the filename from the Label Studio path
    filename = Path(old_path).name
    
    # Check if the image actually exists
    if filename in actual_image_files:
        # Update to just the filename (relative to images_dir)
        img['file_name'] = filename
        valid_images.append(img)
    else:
        missing_images.append(filename)
        print(f"  Skipping missing image: {filename}")

if missing_images:
    print(f"WARNING: {len(missing_images)} images were not found and will be excluded")
    print(f"Valid images: {len(valid_images)}/{len(coco_data['images'])}")
else:
    print(f"All {len(valid_images)} images found!")

# Use only valid images for splitting
images = valid_images
random.shuffle(images)

# Calculate the split index
split_index = int(len(images) * split_ratio)

# Split the images
train_images = images[:split_index]
val_images = images[split_index:]

# Create sets of image IDs for fast lookup
train_image_ids = {img['id'] for img in train_images}
val_image_ids = {img['id'] for img in val_images}

print(f"\nDataset split:")
print(f"  Total valid images: {len(images)}")
print(f"  Training images: {len(train_images)}")
print(f"  Validation images: {len(val_images)}")

# Create new annotation lists
train_annotations = []
val_annotations = []

# Filter annotations based on image IDs
print("\nSplitting annotations...")
for ann in coco_data['annotations']:
    if ann['image_id'] in train_image_ids:
        train_annotations.append(ann)
    elif ann['image_id'] in val_image_ids:
        val_annotations.append(ann)

print(f"  Training annotations: {len(train_annotations)}")
print(f"  Validation annotations: {len(val_annotations)}")

# Create the new COCO JSON structures
train_coco = {
    "info": coco_data.get("info", {}),
    "licenses": coco_data.get("licenses", []),
    "categories": coco_data['categories'],
    "images": train_images,
    "annotations": train_annotations
}

val_coco = {
    "info": coco_data.get("info", {}),
    "licenses": coco_data.get("licenses", []),
    "categories": coco_data['categories'],
    "images": val_images,
    "annotations": val_annotations
}

# Save the new JSON files
print(f"\nSaving training annotations to: {train_json_path}")
with open(train_json_path, 'w') as f:
    json.dump(train_coco, f, indent=4)

print(f"Saving validation annotations to: {val_json_path}")
with open(val_json_path, 'w') as f:
    json.dump(val_coco, f, indent=4)

print("\n✓ Split complete!")

# Verification
print("\nVerification:")
print(f"  Train set: {len(train_images)} images, {len(train_annotations)} annotations")
print(f"  Val set: {len(val_images)} images, {len(val_annotations)} annotations")
if missing_images:
    print(f"  WARNING: {len(missing_images)} images were excluded due to missing files")