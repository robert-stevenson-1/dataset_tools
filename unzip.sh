#!/bin/bash

# Check if a directory path was provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <target_directory_path>"
    echo "Example: $0 /path/to/my/zip/files"
    exit 1
fi

TARGET_DIR="$1"

# Check if the provided directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found."
    exit 1
fi

echo "Starting extraction in directory: $TARGET_DIR"
echo "---"

# Loop through all files in the target directory ending with .zip
# The 'find' command is used here to safely handle all files within the specified directory.
find "$TARGET_DIR" -maxdepth 1 -type f -name "*.zip" | while read -r file; do

    # 1. Determine the filename (just the name, not the path)
    filename=$(basename "$file")
    
    # 2. Determine the destination folder name:
    #    We remove the .zip extension from the filename.
    folder_name="${filename%.zip}" 
    
    # 3. Construct the full path for the new folder
    #    This ensures the new folder is created inside the target directory.
    destination_path="$TARGET_DIR/$folder_name"

    # 4. Create the destination directory.
    echo "Creating directory: $destination_path"
    mkdir -p "$destination_path" 

    # 5. Unzip the file into the new directory:
    #    -q flag for quiet output, -d specifies the destination directory.
    echo "Extracting $filename into $destination_path/"
    unzip -q "$file" -d "$destination_path" 

    echo "" # Add a blank line for readability between files
done

echo "---"
echo "Extraction complete!"