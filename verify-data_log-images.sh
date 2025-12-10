#!/bin/bash

CSV_FILE="combined_data_log.csv"
MISSING_COUNT=0
CHECKED_COUNT=0

# Check if the CSV file exists
if [[ ! -f "$CSV_FILE" ]]; then
    echo "Error: CSV file '$CSV_FILE' not found in the current directory."
    exit 1
fi

echo "Starting verification..."

# Read the CSV file line by line, skipping the header
# IFS=, sets the separator to comma
while IFS=, read -r image_path rest_of_line; do
    # specific handling to strip potential quotes around the path
    clean_path=$(echo "$image_path" | sed 's/^"//;s/"$//')

    # Check if file exists
    if [[ ! -f "$clean_path" ]]; then
        echo "[MISSING] $clean_path"
        ((MISSING_COUNT++))
    fi
    ((CHECKED_COUNT++))

done < <(tail -n +2 "$CSV_FILE")

echo "------------------------------------------------"
echo "Verification complete."
echo "Checked $CHECKED_COUNT files."
if [[ $MISSING_COUNT -eq 0 ]]; then
    echo "SUCCESS: All files exist."
else
    echo "FAILURE: $MISSING_COUNT files are missing."
fi