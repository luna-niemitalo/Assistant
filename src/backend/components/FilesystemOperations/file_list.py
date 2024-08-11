import json
import os
from pathlib import Path

ListFiles_description = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "List files and folders recursively in a specified directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files from."
                },
            },
            "required": ["directory"]
        },
    }
}

def list_files(directory):
    # Ensure the input directory is valid and parse it to be system agnostic
    if not os.path.isdir(directory):
        return json.dumps({"error": f"{directory} is not a valid directory."})

    file_structure = {}

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        # Normalize the path for system agnostic format
        relative_path = os.path.relpath(root, directory)
        file_structure[relative_path] = files

    # Print file structure in JSON format
    return json.dumps(file_structure, indent=2)

if __name__ == "__main__":
    str_path = "C:/dev/Assistant/src/backend/components"
    path = Path(str_path)
    file_structure = list_files(str_path)
    print(file_structure)
