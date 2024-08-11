import json
import os.path
import re
import io
from src.backend.components.Google.google_credentials_create import createGoogleCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from src.backend.components.utils.utils import set_config_path

# Function description for reading a file from Google Drive
ReadGoogleDriveFile_description = {
    "type": "function",
    "function": {
        "name": "read_google_drive_file",
        "description": "Download a file from Google Drive using its URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_url": {
                    "type": "string",
                    "description": "The full URL of the Google Drive file."
                },
            },
            "required": ["file_url"]
        },
    },
}

def extract_file_id(file_url):
    """Extract the file ID from a Google Drive URL."""
    match = re.search(r'drive\.google\.com/file/d/([^/]+)', file_url)
    return match.group(1) if match else None

def read_google_drive_file(file_url):
    """Download a file from Google Drive and return its content."""
    file_id = extract_file_id(file_url)
    if not file_id:
        return json.dumps({"error": "Invalid Google Drive file URL."})
    
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]
    
    try:
        service = build("drive", "v3", credentials=creds)

        # Request to get the file
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}% complete.")

        file_stream.seek(0)
        content = file_stream.read()
        return content.decode('utf-8')  # Assuming the content is text

    except HttpError as err:
        return json.dumps({"error": str(err)})

if __name__ == "__main__":
    set_config_path()


    # Example usage with a file URL
    file_url = "https://docs.google.com/document/d/1JSt1Pp5nfegJdYQTRzb4tF3y9E6GTSWG9w3PoNN95Ro/edit"
    result = read_google_drive_file(file_url)
    print(result)