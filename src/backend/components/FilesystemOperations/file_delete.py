import os
import json

DeleteFile_description = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "description": "Deletes a specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to delete."
                }
            },
            "required": ["file_path"]
        }
    }
}

def backup_existing_file(file_path):
    # This function checks if the file exists and creates a backup if it does
    if os.path.exists(file_path):
        # Get the directory and filename details
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        backup_directory = os.path.join(directory, "AI_write_backups")

        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        # Find all existing backup files and count them
        backups = [f for f in os.listdir(backup_directory) if f.startswith(filename + ".bac_")]
        backup_number = len(backups)

        # Create backup filename
        backup_filename = f"{filename}.bac_{backup_number + 1}"
        backup_path = os.path.join(backup_directory, backup_filename)

        # Copy the existing file to backup location
        os.rename(file_path, backup_path)

        print(f"Backup created: {backup_path}")

    else:
        print(f"No existing file to backup.")


def delete_file(file_path):
    """
    Deletes a file at the specified path.
    :param file_path: The path of the file to delete.
    """
    if not os.path.isfile(file_path):
        return json.dumps({"error": f"{file_path} is not a valid file."})
    try:
        backup_existing_file(file_path)
        return json.dumps({"message": f"File {file_path} has been deleted successfully."})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    str_file_path = "C:/dev/Assistant/src/backend/components/example.txt"

    result = delete_file(str_file_path)
    print(result)