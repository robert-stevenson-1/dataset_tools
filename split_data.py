"""
==================================================================================================
Dataset Splitter (YOLOv5)

Purpose:
This script takes a dataset exported from a tool like Label Studio (which doesn't create
train/val splits) and organises it into the directory structure required by YOLOv5.

How it works:
1. It reads a list of all image files from a source directory.
2. It randomly shuffles this list.
3. It splits the list into training and validation sets based on a defined ratio.
4. It creates the necessary 'train' and 'val' subdirectories for both images and labels.
5. It moves each image and corresponding YOLO (.txt) label file to the correct
   destination folder.

Instructions:
1. Place this script in a 'workspace' directory.
2. Place your 'images' and 'labels' folders inside the same workspace from Label Studio.
3. Adjust the configuration variables below (source/output directories and split ratio).
4. Run the script from your terminal: python split_data.py
==================================================================================================
"""

import os
import random
import shutil

# --- Configuration ---
# Set the paths to your source images and labels folders
source_images_dir = 'images'
source_labels_dir = 'labels'

# Set the path for the new dataset directory that will be created
output_dir = 'final_dataset'

# Set the split ratio for training data (e.g., 0.8 for 80%)
# The rest will be used for validation.
train_split_ratio = 0.8
# ---------------------


# Create the necessary output directories
def create_dirs(base_path):
    os.makedirs(os.path.join(base_path, 'images/train'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'images/val'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'labels/train'), exist_ok=True)
    os.makedirs(os.path.join(base_path, 'labels/val'), exist_ok=True)

def split_dataset():
    print(f"Creating output directories at: {output_dir}")
    create_dirs(output_dir)

    # Get a list of all image files (assuming they have common extensions)
    image_files = [f for f in os.listdir(source_images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Shuffle the list of files randomly
    random.shuffle(image_files)
    
    # Calculate the split index
    split_index = int(len(image_files) * train_split_ratio)
    
    # Divide the files into training and validation sets
    train_files = image_files[:split_index]
    val_files = image_files[split_index:]
    
    print(f"Found {len(image_files)} total images.")
    print(f"Splitting into {len(train_files)} training images and {len(val_files)} validation images.")

    # Function to move files
    def move_files(file_list, dest_folder):
        for filename in file_list:
            # Get the base name of the file without the extension
            base_filename = os.path.splitext(filename)[0]
            
            # Construct source and destination paths for the image
            src_image_path = os.path.join(source_images_dir, filename)
            dest_image_path = os.path.join(output_dir, 'images', dest_folder, filename)
            
            # Construct source and destination paths for the label
            src_label_path = os.path.join(source_labels_dir, base_filename + '.txt')
            dest_label_path = os.path.join(output_dir, 'labels', dest_folder, base_filename + '.txt')

            # Move the image
            shutil.move(src_image_path, dest_image_path)
            
            # Move the corresponding label file, if it exists
            if os.path.exists(src_label_path):
                shutil.move(src_label_path, dest_label_path)

    # Move the files to their respective directories
    print("\nMoving training files...")
    move_files(train_files, 'train')
    
    print("\nMoving validation files...")
    move_files(val_files, 'val')
    
    print("\nDataset split complete!")

if __name__ == '__main__':
    split_dataset()
