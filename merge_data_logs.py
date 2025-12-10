import pandas as pd
import re
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# List all your CSV files here. 
# You can add the paths to your bottle data logs.
file_list = [
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_1/data_log.csv',
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_2/data_log.csv',
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_3/data_log.csv',
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_4/data_log.csv',
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_5/data_log.csv',
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_6/data_log.csv',
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_7/data_log.csv',
    '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/bottle_8/data_log.csv'
]

# ---------------------------------------------------------
# FUNCTION DEFINITIONS
# ---------------------------------------------------------
def transform_image_path(path):
    """
    Parses the original path (e.g., ./data/v2/bottle_1/00000.jpg)
    and converts it to the new format (e.g., ./images/B1-00000.jpg).
    """
    # Regex to find 'bottle_X' and the filename
    # Looks for pattern: .../bottle_{number}/{filename}
    match = re.search(r'bottle_(\d+)[/\\]([^/\\]+)$', path)
    
    if match:
        bottle_num = match.group(1) # e.g., '1'
        filename = match.group(2)   # e.g., '00000_25112025.jpg'
        
        # Construct new filename with B{id} prefix
        new_filename = f"B{bottle_num}-{filename}"
        
        # Construct new full path
        new_path = f"./images/{new_filename}"
        return new_path
    
    # Return original path if pattern not found
    return path

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
dataframes = []

for file_path in file_list:
    if os.path.exists(file_path):
        print(f"Processing: {file_path}")
        df = pd.read_csv(file_path)
        dataframes.append(df)
    else:
        print(f"Warning: File not found - {file_path}")

if dataframes:
    # 1. Combine all dataframes
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # 2. Apply the path transformation
    # We verify the transformation on the 'image_path' column
    combined_df['image_path'] = combined_df['image_path'].apply(transform_image_path)
    
    # 3. Save the result
    output_filename = '/root/zfs-crow-compute/datasets/PCN/v2/Original_copy/combined_data_log.csv'
    combined_df.to_csv(output_filename, index=False)
    
    print(f"\nSuccess! Combined data saved to '{output_filename}'.")
    print(f"Total rows: {len(combined_df)}")
    
    # Display a preview of the updated paths
    print("\nPreview of updated paths:")
    print(combined_df['image_path'].head())

else:
    print("No dataframes to combine. Please check your file paths.")