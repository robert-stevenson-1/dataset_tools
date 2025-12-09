import os
import json
import shutil
from pathlib import Path

# --- CONFIGURATION ---
# List the directories you want to process and their new prefixes
# Format: { "Folder_Name": "New_Prefix" }
DATASETS_TO_PROCESS = {
    "B1-COCO": "B1",
    "B2-COCO": "B2",
    "B3-COCO": "B3",
    "B4-COCO": "B4",
    "B5-COCO": "B5",
    "B6-COCO": "B6",
    "B7-COCO": "B7",
    "B8-COCO": "B8",
}
# ---------------------

def process_dataset(folder_name, new_prefix):
    root_path = Path(folder_name)
    json_path = root_path / 'result.json'
    images_dir = root_path / 'images'

    if not json_path.exists():
        print(f"Skipping {folder_name}: result.json not found.")
        return

    print(f"--- Processing {folder_name} (Prefix: {new_prefix}) ---")

    # 1. Load the COCO JSON
    with open(json_path, 'r') as f:
        coco_data = json.load(f)

    # 2. Iterate through images to rename them
    renamed_count = 0
    
    for image_entry in coco_data['images']:
        # current path in JSON (e.g., "images/1257_hash-000_25.jpg" or absolute path)
        original_json_path = image_entry['file_name']
        
        # Get just the filename (e.g., "1257_hash-000_25.jpg")
        original_filename = os.path.basename(original_json_path)
        
        # --- NAMING LOGIC ---
        # We split by the first hyphen '-' to separate LabelStudio ID from original name
        # Input: 1257_4664fbd6-00000_25112025.jpg
        parts = original_filename.split('-', 1)
        
        if len(parts) < 2:
            print(f"Warning: Filename structure unexpected, skipping: {original_filename}")
            continue
            
        # parts[0] is "1257_4664fbd6"
        # parts[1] is "00000_25112025.jpg"
        suffix = parts[1]
        
        # Construct new name: "B1-00000_25112025.jpg"
        new_filename = f"{new_prefix}-{suffix}"
        
        # --------------------

        # Define full physical paths
        old_file_path = images_dir / original_filename
        new_file_path = images_dir / new_filename

        # A. Rename the physical file
        if old_file_path.exists():
            # If we've already run this script, checking existence prevents errors
            if old_file_path != new_file_path:
                os.rename(old_file_path, new_file_path)
        elif new_file_path.exists():
             # File already renamed, just update JSON
             pass
        else:
            print(f"Error: Image file not found on disk: {original_filename}")
            continue

        # B. Update the JSON entry
        # We assume you want the relative path "images/filename.jpg" in the JSON
        image_entry['file_name'] = f"images/{new_filename}"
        renamed_count += 1

    # 3. Save the updated JSON
    # We save to a new file first to be safe, then you can rename it if satisfied
    output_json_path = root_path / 'result_renamed.json'
    with open(output_json_path, 'w') as f:
        json.dump(coco_data, f, indent=2)

    print(f"Success! Renamed {renamed_count} images.")
    print(f"Saved updated annotations to: {output_json_path}")
    
    # Optional: Overwrite original result.json automatically
    shutil.move(output_json_path, json_path)
    print("Overwrote original result.json")

if __name__ == "__main__":
    for folder, prefix in DATASETS_TO_PROCESS.items():
        if os.path.exists(folder):
            process_dataset(folder, prefix)
        else:
            print(f"Directory not found: {folder}")