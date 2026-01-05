import json

# --- User Configuration ---

# The name of the JSON file you are copying annotations FROM.
SOURCE_JSON_FILE = 'project-12-at-2025-11-02-20-11-04ae73e6.json'

# The name of the NEW JSON file that will be created with the annotations.
OUTPUT_JSON_FILE = 'annotations.json'

# The name of the text file containing the list of filenames (one per line).
FILENAMES_TEXT_FILE = 'sorted_image_list.txt'

# The ID of the task in the source file that has the annotations you want to copy.
SOURCE_TASK_ID = 224

# ✨ NEW: Change this number for the "/data/upload/[number]/" path in the output.
UPLOAD_DIRECTORY_NUMBER = 12 

# --- End of User Configuration ---


def create_new_annotation_file():
    """
    Creates a new JSON file by applying a set of source annotations to a list
    of filenames provided in a text file, using a customizable upload path.
    """
    print(f"Reading source annotations from '{SOURCE_JSON_FILE}'...")

    # 1. Read the source JSON file to get the annotations
    try:
        with open(SOURCE_JSON_FILE, 'r') as f:
            all_tasks = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: The source file '{SOURCE_JSON_FILE}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: The file '{SOURCE_JSON_FILE}' is not a valid JSON file.")
        return

    # 2. Find the task with the annotations we want to copy
    source_task = next((task for task in all_tasks if task.get('id') == SOURCE_TASK_ID), None)
    if not source_task:
        print(f"❌ Error: Task with ID '{SOURCE_TASK_ID}' not found in the source JSON.")
        return

    # 3. Extract the list of annotation results (the bounding boxes)
    try:
        source_annotations_result = source_task['annotations'][0]['result']
        print(f"✅ Found {len(source_annotations_result)} annotations to copy from task ID {SOURCE_TASK_ID}.")
    except (IndexError, KeyError):
        print(f"❌ Error: Could not find any annotations to copy for task ID {SOURCE_TASK_ID}.")
        return

    # 4. Read the target filenames from the text file
    try:
        with open(FILENAMES_TEXT_FILE, 'r') as f:
            target_filenames = [line.strip() for line in f if line.strip()]
        if not target_filenames:
            print(f"🤷 The file '{FILENAMES_TEXT_FILE}' is empty. No output file will be created.")
            return
        print(f"Found {len(target_filenames)} filenames in '{FILENAMES_TEXT_FILE}'.")
    except FileNotFoundError:
        print(f"❌ Error: The file '{FILENAMES_TEXT_FILE}' was not found. Please create it.")
        return

    # 5. Build the list of new tasks for the output file
    newly_annotated_tasks = []
    print("\nGenerating new tasks...")
    for i, filename in enumerate(target_filenames):
        new_task_id = i + 1  # Simple sequential IDs for the new file
        
        # This line now uses the customizable UPLOAD_DIRECTORY_NUMBER
        image_path = f"/data/upload/{UPLOAD_DIRECTORY_NUMBER}/{filename}"
        
        new_task = {
            "id": new_task_id,
            "file_upload": filename,
            "data": {
                "image": image_path
            },
            "annotations": [
                {
                    "result": source_annotations_result
                }
            ],
            "predictions": []
        }
        
        newly_annotated_tasks.append(new_task)
        print(f"   + Created task for '{filename}' with path '{image_path}'.")

    # 6. Write the newly created tasks to the output JSON file
    try:
        with open(OUTPUT_JSON_FILE, 'w') as f:
            json.dump(newly_annotated_tasks, f, indent=4)
        print(f"\n🎉 Success! A new file was created: '{OUTPUT_JSON_FILE}'")
        print(f"It contains annotations for {len(newly_annotated_tasks)} image(s).")
    except IOError as e:
        print(f"❌ Error writing to file '{OUTPUT_JSON_FILE}': {e}")


if __name__ == "__main__":
    create_new_annotation_file()