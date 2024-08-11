import json
import os

WriteFile_description = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write content to a specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to write."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                },
            },
            "required": ["file_path", "content"]
        },
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


def write_file(file_path, content):
    # Ensure to backup existing file
    backup_existing_file(file_path)

    # Ensure the input file path is valid
    try:
        with open(file_path, 'w') as file:
            file.write(content)
            return json.dumps({"message": f"Content written to {file_path} successfully."})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    str_file_path = "C:/dev/Assistant/src/backend/components/example.txt"
    str_content = "This is an example content written to the file 10."
    result = write_file(str_file_path, str_content)
    print(result)
