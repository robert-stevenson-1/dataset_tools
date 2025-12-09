import json
import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
# List of input folders (the ones you just cleaned)
INPUT_DATASETS = [
    "B1-COCO", "B2-COCO", "B3-COCO", "B4-COCO", 
    "B5-COCO", "B6-COCO", "B7-COCO", "B8-COCO"
]

OUTPUT_DIR = "B1-8-COCO"

# Which JSON file to look for in the input folders?
# If you ran the previous script but didn't rename the result file, use 'result_renamed.json'
TARGET_JSON_NAME = "result_renamed.json" 
# ---------------------

def merge_datasets():
    output_path = Path(OUTPUT_DIR)
    output_images_dir = output_path / 'images'
    output_images_dir.mkdir(parents=True, exist_ok=True)

    # Initialize the Master JSON structure
    master_coco = {
        "images": [],
        "annotations": [],
        "categories": [],
        "info": {"description": "Merged Dataset B1-8"},
        "licenses": []
    }

    # Tracking Global IDs to prevent collisions
    global_image_id = 1
    global_ann_id = 1
    
    # Map Category Names to Global IDs to ensure consistency
    # e.g. {"bottle": 1, "cap": 2}
    category_name_to_id = {}
    next_category_id = 0

    print(f"Starting merge of {len(INPUT_DATASETS)} datasets into {OUTPUT_DIR}...")

    for dataset_folder in INPUT_DATASETS:
        dataset_path = Path(dataset_folder)
        json_file = dataset_path / TARGET_JSON_NAME
        
        # Fallback to result.json if renamed version doesn't exist
        if not json_file.exists():
            json_file = dataset_path / 'result.json'
            
        if not json_file.exists():
            print(f"Skipping {dataset_folder}: No JSON found.")
            continue

        print(f"Processing {dataset_folder}...")

        with open(json_file, 'r') as f:
            data = json.load(f)

        # 1. Map Categories for this specific dataset
        # We need a local map because Dataset 1 might have "Bottle"=0 
        # and Dataset 2 might have "Bottle"=5. We need to standardize.
        local_cat_id_to_global = {}
        
        for cat in data.get('categories', []):
            cat_name = cat['name']
            
            # If we haven't seen this category name before, add it to master
            if cat_name not in category_name_to_id:
                category_name_to_id[cat_name] = next_category_id
                master_coco['categories'].append({
                    "id": next_category_id,
                    "name": cat_name
                })
                next_category_id += 1
            
            # Map the local ID to the global ID
            global_id = category_name_to_id[cat_name]
            local_cat_id_to_global[cat['id']] = global_id

        # 2. Process Images
        # Map local image IDs to new global IDs
        local_img_id_to_global = {}

        for img in data['images']:
            # Setup Paths
            filename = os.path.basename(img['file_name'])
            src_image_path = dataset_path / 'images' / filename
            dst_image_path = output_images_dir / filename

            # Copy image file
            if src_image_path.exists():
                shutil.copy2(src_image_path, dst_image_path)
            else:
                print(f"  Warning: Image missing {src_image_path}")
                continue

            # Update Image Metadata
            new_img = img.copy()
            new_img['id'] = global_image_id
            # Ensure path is standard relative path
            new_img['file_name'] = f"images/{filename}" 
            
            master_coco['images'].append(new_img)
            
            # Map old ID to new ID
            local_img_id_to_global[img['id']] = global_image_id
            global_image_id += 1

        # 3. Process Annotations
        for ann in data['annotations']:
            new_ann = ann.copy()
            
            # Update IDs
            new_ann['id'] = global_ann_id
            
            # Link to the new Image ID
            old_img_id = ann['image_id']
            if old_img_id not in local_img_id_to_global:
                # This happens if the image was missing and we skipped it
                continue
            new_ann['image_id'] = local_img_id_to_global[old_img_id]

            # Link to the new Category ID
            old_cat_id = ann['category_id']
            new_ann['category_id'] = local_cat_id_to_global[old_cat_id]

            master_coco['annotations'].append(new_ann)
            global_ann_id += 1

    # Save Master JSON
    output_json = output_path / 'result.json'
    with open(output_json, 'w') as f:
        json.dump(master_coco, f, indent=2)

    print(f"--- Merge Complete ---")
    print(f"Total Images: {len(master_coco['images'])}")
    print(f"Total Annotations: {len(master_coco['annotations'])}")
    print(f"Categories Found: {list(category_name_to_id.keys())}")
    print(f"Saved to: {output_json}")

if __name__ == "__main__":
    merge_datasets()