#!/bin/bash

# Replace YOUR_LABEL_STUDIO_TOKEN_HERE with the actual token you copied.
LABEL_STUDIO_TOKEN="${LABEL_STUDIO_TOKEN}" 
EXPORT_FORMAT="JSON"
PROJECT_ID="27"
BASE_URL="http://192.168.1.176:80"

FILE_EXTENSION=".zip"
if [ "$EXPORT_FORMAT" == "JSON" ]; then
    FILE_EXTENSION=".json"
fi

# Construct the output filename.
OUTPUT_FILENAME="project_${PROJECT_ID}_${EXPORT_FORMAT}_export${FILE_EXTENSION}"

# Construct the URL.
EXPORT_URL="${BASE_URL}/api/projects/${PROJECT_ID}/export?exportType=${EXPORT_FORMAT}&download_all_tasks=true"

echo "Starting Label Studio export for Project $PROJECT_ID in ${EXPORT_FORMAT} format..."

# Execute the cURL command to download the export.
# The token is passed in the Authorization header.
curl -X GET \
    -H "Authorization: Token ${LABEL_STUDIO_TOKEN}" \
    --output "$OUTPUT_FILENAME" \
    "$EXPORT_URL"

# Check the exit status of the previous command (cURL)
if [ $? -eq 0 ]; then
    echo "Success: ${EXPORT_FORMAT} export downloaded and saved to $OUTPUT_FILENAME"
else
    echo "Error: The export failed. Check your token, URL, and project ID."
fi