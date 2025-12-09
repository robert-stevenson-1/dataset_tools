import json
import copy
import os

# --- CONFIGURATION ---
# Change these values to match your filenames and IDs
INPUT_FILENAME = 'project_27_JSON_export.json'              # Take and enter the file name of the JSON output file from `download_project_annotations.sh`
OUTPUT_FILENAME = 'project_27_JSON_export_copied.json'      # The new file to create
SOURCE_ID_TO_COPY = 1173                                    # The ID you want to copy FROM in the input file

def distribute_annotations(input_file, output_file, source_id):
    """
    Copies annotations from a specific ID to all other tasks in the JSON file.
    """
    
    # 1. Load the JSON data
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' was not found.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file format.")
        return

    # 2. Find the source annotations
    source_annotations = None
    
    for task in data:
        if task.get('id') == source_id:
            # We use deepcopy to ensure we get a clean snapshot of the data
            source_annotations = copy.deepcopy(task.get('annotations', []))
            print(f"Found source ID {source_id}. Annotations extracted.")
            break
            
    if source_annotations is None:
        print(f"Error: ID {source_id} was not found in the file.")
        return

    # 3. Apply annotations to all tasks
    count = 0
    for task in data:
        # Skip the source ID (though its harmless to overwrite)
        if task.get('id') == source_id: continue
        
        # deepcopy again so every task gets its own independent list object
        task['annotations'] = copy.deepcopy(source_annotations)
        count += 1

    # 4. Save the modified data
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Success! Copied annotations to {count} tasks.")
        print(f"Saved to: {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")


# Run the function
if __name__ == "__main__":
    distribute_annotations(INPUT_FILENAME, OUTPUT_FILENAME, SOURCE_ID_TO_COPY)