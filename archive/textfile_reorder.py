# Define the names for the input and output files
input_filename = 'image_list.txt'
output_filename = 'sorted_image_list.txt'

try:
    # --- 1. Read all filenames from the input file ---
    # 'with open' ensures the file is automatically closed even if errors occur.
    with open(input_filename, 'r') as file:
        # Read all lines into a list and use .strip() to remove any extra
        # whitespace or newline characters from the beginning or end of each line.
        original_filenames = [line.strip() for line in file if line.strip()]

    # --- 2. Sort the list of filenames ---
    # The key tells the sort function to look only at the part of the
    # filename that comes after the first hyphen '-'.
    sorted_filenames = sorted(original_filenames, key=lambda filename: filename.split('-')[1])

    # --- 3. Write the sorted list to a new file ---
    with open(output_filename, 'w') as file:
        # Go through each filename in the sorted list...
        for name in sorted_filenames:
            # ...and write it to the new file, adding a newline character at the end.
            file.write(name + '\n')
    
    print(f"✅ Success! Sorted filenames have been saved to '{output_filename}'.")

except FileNotFoundError:
    print(f"❌ Error: The file '{input_filename}' was not found.")
    print("Please make sure the script is in the same directory as your text file.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")