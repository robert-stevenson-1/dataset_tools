"""
==================================================================================================
YOLOv5 Dataset Preparation Script (with Train/Val/Test Split)

Purpose:
This script automates the key preparation steps for a robust YOLOv5 workflow:
1.  **Splitting Data**: It takes a flat directory of images and labels and splits them into
    'train', 'val', and 'test' sets according to specified ratios.
2.  **Creating YAML**: It automatically generates the 'dataset.yaml' file required by
    YOLOv5, populating it with the correct paths, class count, and class names.

Instructions:
1.  **MUST DO**: Edit the `class_names` list below to match your dataset's classes in the
    exact order they were defined in your labeling tool.
2.  **MUST DO**: Adjust the `train_ratio` and `val_ratio`. The remaining percentage will
    be automatically used for the 'test' set.
3.  Place this script in a 'workspace' directory.
4.  Inside the same workspace, place your 'images' and 'labels' folders.
5.  Run the script from your terminal: python prepare_yolo_dataset.py
==================================================================================================
"""
import os
import random
import shutil

# --- Configuration ---
# EDIT THIS LIST to match your class names in the correct order.
class_names = ['cyst']

# Set the ratios for splitting the data. The rest will be used for the test set.
train_ratio = 0.7  # 70% of data for training
val_ratio = 0.2    # 20% of data for validation
# test_ratio will be automatically calculated as 1.0 - train_ratio - val_ratio (which is 10% in this case)

# Set the paths to your source images and labels folders
source_images_dir = '../images'
source_labels_dir = '../labels'

# Set the path for the new dataset directory that will be created (!update to suit your needs)
output_dir = '/root/zfs-crow-compute/datasets/PCN/bottle-1/final_dataset'
# ---------------------


def create_yaml_file(output_dir, class_names_list):
    """Creates the dataset.yaml file."""
    nc = len(class_names_list)
    
    yaml_content = f"""
# YOLOv5 dataset configuration file
# Created by prepare_yolo_dataset.py

# Paths to train/val/test image directories (relative to yolov5/ directory)
train: ../{output_dir}/images/train/
val: ../{output_dir}/images/val/
test: ../{output_dir}/images/test/

# ---
# Number of classes
nc: {nc}

# Class names
names: {class_names_list}
"""
    
    yaml_file_path = os.path.join(output_dir, 'dataset.yaml')
    with open(yaml_file_path, 'w') as f:
        f.write(yaml_content)
        
    print(f"\n✅ Successfully created {yaml_file_path}")
    print(f"👉 Your YOLOv5 --data argument should be: {yaml_file_path}")


def split_dataset():
    """Splits the dataset and creates the YAML file."""
    # Basic validation of inputs
    if not class_names:
        print("❌ Error: The 'class_names' list is empty. Please edit the script to add your class names.")
        return
    if (train_ratio + val_ratio) >= 1.0:
        print(f"❌ Error: The sum of train_ratio ({train_ratio}) and val_ratio ({val_ratio}) must be less than 1.0.")
        return

    print("🚀 Starting dataset preparation...")
    
    # Create the necessary output directories
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'labels', split), exist_ok=True)

    # Get a list of all image files and shuffle them
    image_files = [f for f in os.listdir(source_images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(image_files)
    
    # Calculate split indices
    total_files = len(image_files)
    train_end = int(total_files * train_ratio)
    val_end = train_end + int(total_files * val_ratio)
    
    # Divide the files into sets
    train_files = image_files[:train_end]
    val_files = image_files[train_end:val_end]
    test_files = image_files[val_end:]
    
    print(f"\nFound {total_files} total images. Splitting into:")
    print(f"  - Training:   {len(train_files)} images")
    print(f"  - Validation: {len(val_files)} images")
    print(f"  - Test:       {len(test_files)} images")

    # Function to move files
    def copy_files(file_list, dest_folder):
        for filename in file_list:
            base_filename = os.path.splitext(filename)[0]
            shutil.copy(os.path.join(source_images_dir, filename), os.path.join(output_dir, 'images', dest_folder, filename))
            label_file = base_filename + '.txt'
            if os.path.exists(os.path.join(source_labels_dir, label_file)):
                shutil.copy(os.path.join(source_labels_dir, label_file), os.path.join(output_dir, 'labels', dest_folder, label_file))

    # Move the files
    print("\nCopying files...")
    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    copy_files(test_files, 'test')
    
    # Create the YAML file
    create_yaml_file(output_dir, class_names)
    
    print("\n🎉 Dataset preparation complete!")


if __name__ == '__main__':
    split_dataset()