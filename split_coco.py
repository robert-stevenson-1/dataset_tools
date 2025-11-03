import json
import random
import os

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

# --- End Configuration ---

# Construct full paths
original_json_path = os.path.join(data_root, original_json_name)
train_json_path = os.path.join(data_root, train_json_name)
val_json_path = os.path.join(data_root, val_json_name)

print(f"Loading original annotations from: {original_json_path}")

# Load the original COCO JSON
with open(original_json_path, 'r') as f:
    coco_data = json.load(f)

# Get all images and shuffle them
images = coco_data['images']
random.shuffle(images)

# Calculate the split index
split_index = int(len(images) * split_ratio)

# Split the images
train_images = images[:split_index]
val_images = images[split_index:]

# Create sets of image IDs for fast lookup
train_image_ids = {img['id'] for img in train_images}
val_image_ids = {img['id'] for img in val_images}

print(f"Total images: {len(images)}")
print(f"Training images: {len(train_images)}")
print(f"Validation images: {len(val_images)}")

# Create new annotation lists
train_annotations = []
val_annotations = []

# Filter annotations based on image IDs
print("Splitting annotations...")
for ann in coco_data['annotations']:
    if ann['image_id'] in train_image_ids:
        train_annotations.append(ann)
    elif ann['image_id'] in val_image_ids:
        val_annotations.append(ann)

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
print(f"Saving training annotations to: {train_json_path}")
with open(train_json_path, 'w') as f:
    json.dump(train_coco, f, indent=4)

print(f"Saving validation annotations to: {val_json_path}")
with open(val_json_path, 'w') as f:
    json.dump(val_coco, f, indent=4)

print("Split complete!")