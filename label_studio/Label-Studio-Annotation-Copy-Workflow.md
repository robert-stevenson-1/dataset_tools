# Label Studio Annotation Copying Workflow

A guide/reminded to myself for the two steps for exporting annotations from Label Studio's project and copying a set of annotations from one task to all other tasks.

## Required Files

1.  `dowload_project_annotations.sh`: Used to download the JSON export of your project's annotations.
2.  `copy_annotations.py`: A Python script used to process the downloaded file and copy annotations from a source task ID to all other tasks.


## Step 1: Configure and Download Annotations

First, configure the bash script and download the project data.

### Configure `dowload_project_annotations.sh`

Open `dowload_project_annotations.sh` and update the variables with specific project details needed:

  * `LABEL_STUDIO_TOKEN`: Replace `"YOUR_LABEL_STUDIO_TOKEN_HERE"` with your actual Label Studio API token or from your system environment variables.
  * `PROJECT_ID`: Set this to the ID of the project you are exporting (e.g., `"27"`).
  * `BASE_URL`: Set this to the URL of your Label Studio instance (e.g., `"http://192.168.1.176:80"` in my case).

The script is configured to export in `JSON` format, which is required for the Python script.
_It can also export `COCO` if desired, but copying doesn't do this_

### B. Run the Download Script

1.  **Make the script executable**:
    ```bash
    chmod +x dowload_project_annotations.sh
    ```
2.  **Run the script**:
    ```bash
    ./dowload_project_annotations.sh
    ```

**Output:** This step will create a file named `project_<PROJECT_ID>_JSON_export.json` (e.g., `project_27_JSON_export.json`) in the same directory.
_or if `COCO`, just a zip file (but no images are downloaded with it)_

-----

## Step 2: Configure and Copy Annotations

use the Python script to process the downloaded file.

### Configure `copy_annotations.py`

update `copy_annotations.py` configuration section near top:

| Variable | Current Value (in script) | Description |
| :--- | :--- | :--- |
| `INPUT_FILENAME` | `'project_27_JSON_export.json'` | **Must match the filename created in Step 1**. |
| `OUTPUT_FILENAME` | `'project_27_JSON_export_copied.json'` | The new file the results will be saved to. |
| `SOURCE_ID_TO_COPY` | `1173` | **The ID (Task ID) whose annotations you want to copy to all other tasks**. |

### B. Run the Python Script

Execute the Python script using a local interpreter:

```bash
python3 copy_annotations.py
```

**Output:** The script confirms that it has found the source ID and copies and saves the new file to the `OUTPUT_FILENAME` (e.g., `project_27_JSON_export_copied.json`).

### Result

The output file should contain the annotations for all images from the project. Import this file back into Label Studio in a new project (just in case).
