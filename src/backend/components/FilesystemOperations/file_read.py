import json
import os

ReadFile_description = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the content of a specified file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to read."
                },
            },
            "required": ["file_path"]
        },
    }
}

def read_file(file_path):
    # Ensure the input file path is valid
    if not os.path.isfile(file_path):
        return json.dumps({"error": f"{file_path} is not a valid file."})

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return json.dumps({"content": content})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    str_file_path = "C:/dev/Assistant/src/backend/components/ReadFile.py"
    file_content = read_file(str_file_path)
    print(file_content)