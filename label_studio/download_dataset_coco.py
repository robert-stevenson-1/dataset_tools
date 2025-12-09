import os
import json
import requests
from pathlib import Path
from label_studio_sdk import Client
from label_studio_converter import Converter

# --- CONFIGURATION ---
LABEL_STUDIO_URL = 'http://192.168.1.176:80'  # Your Label Studio URL
# If the variable isn't found, this returns None (or you can set a default)
API_KEY = os.getenv('LABEL_STUDIO_TOKEN')   # Your API Key
PROJECT_ID = 1                              # The Project ID you want to export
BOTTLE_ID = 1                               # Specific to my needs and folder generation when batch processing
OUTPUT_DIR = f'B{BOTTLE_ID}-COCO'          # Where to save the data
# ---------------------

if not API_KEY:
    raise ValueError("Error: LABEL_STUDIO_TOKEN environment variable is not set.")

def export_coco_with_images():
    # 1. Setup & Connection
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    project = ls.get_project(PROJECT_ID)
    
    # Create output directories
    output_path = Path(OUTPUT_DIR)
    images_dir = output_path / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Fetching data for Project {PROJECT_ID}...")

    # 2. Create a NEW Snapshot, then Download it
    # We split this into two steps to avoid the TypeError
    
    # Step A: Create the snapshot
    snapshot = project.export_snapshot_create(
        title='Auto Export COCO'
    )
    export_id = snapshot['id']
    print(f"Snapshot created with ID: {export_id}")

    # Step B: Download it using the ID
    # Note: We assume the file creates a file named after the project/time
    # The SDK downloads it to the 'path' directory.
    downloaded_filename = project.export_snapshot_download(
        export_id=export_id,
        export_type='JSON',
        path=str(output_path)
    )
    
    # Verify if SDK returned a tuple (success, filename) or just filename
    if isinstance(downloaded_filename, tuple):
        downloaded_filename = downloaded_filename[1] 

    # --- THE FIX IS HERE ---
    # Combine the directory (output_path) with the filename
    full_json_path = output_path / downloaded_filename

    with open(full_json_path, 'r') as f:
        tasks = json.load(f)

    print(f"Downloaded {len(tasks)} tasks. Downloading images...")

    # 3. Download Images & Update Paths
    # We must download images so the Converter can read their dimensions (required for COCO)
    headers = {'Authorization': f'Token {API_KEY}'}
    
    for task in tasks:
        # Extract image URL (supports different data key names usually 'image' or 'url')
        image_url = task['data'].get('image') or task['data'].get('url')
        
        if not image_url:
            continue

        # Handle simplified relative paths (e.g., /data/upload/...)
        if image_url.startswith('/'):
            full_url = f"{LABEL_STUDIO_URL}{image_url}"
        else:
            full_url = image_url

        # Generate a safe local filename
        # We use the ID to ensure uniqueness if filenames are duplicate
        file_name = os.path.basename(image_url.split('?')[0]) 
        local_filename = f"{task['id']}_{file_name}"
        local_path = images_dir / local_filename

        # Download the image if it doesn't exist
        if not local_path.exists():
            try:
                r = requests.get(full_url, headers=headers, stream=True)
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            except Exception as e:
                print(f"Failed to download {full_url}: {e}")
                continue

        # CRITICAL: Update the task data to point to the local file
        # The converter needs this to read image width/height
        task['data']['image'] = str(local_path.absolute())

    # Save the updated JSON with local paths (temporary file)
    temp_json_path = output_path / 'temp_local_tasks.json'
    with open(temp_json_path, 'w') as f:
        json.dump(tasks, f)

    # 4. Convert to COCO
    print("Converting to COCO format...")
    
    try:
        project_config = project.get_params()['label_config']
        converter = Converter(config=project_config, project_dir=None)
        
        # FIX: Pass paths as positional arguments (without "input_data=" or "output_file=")
        converter.convert_to_coco(
            str(temp_json_path),                 # Arg 1: Input file path
            str(output_path),    # Arg 2: Output file path
            output_image_dir=str(images_dir),    # Arg 3: Image directory (keyword ok)
            is_dir=False
        )
        print(f"SUCCESS: Project {PROJECT_ID} saved to {output_path}/result.json")
    except Exception as e:
        print(f"Conversion failed for {PROJECT_ID}: {e}")
        # Optional: print full traceback to debug deep errors
        import traceback
        traceback.print_exc()

    # Cleanup temp file
    if os.path.exists(temp_json_path):
        os.remove(temp_json_path)

    print(f"SUCCESS: Export saved to {output_path}/result.json")

if __name__ == "__main__":
    for i in range(1, 9):
        PROJECT_ID = i + 28
        BOTTLE_ID = 9 - i
        OUTPUT_DIR = f'B{BOTTLE_ID}-COCO'          # Where to save the data
        export_coco_with_images()
        print("\n============\n")