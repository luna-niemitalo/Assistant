import json
import os.path
import io
from src.backend.components.CreateGoogleCredentials import createGoogleCredentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

SaveFileToDrive_description = {
    "type": "function",
    "function": {
        "name": "save_file_to_drive",
        "description": "Saves a specified file to Google Drive within the App Folder scope. "
                       "Returns a confirmation message upon successful upload.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "The name of the file to save."
                },
                "file_content": {
                    "type": "string",
                    "description": "The content of the file to save, in string format."
                }
            },
            "required": ["file_name", "file_content"],
        },
    }
}

def list_files():
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)

    creds = creds["message"]

    try:
        # call drive api client
        service = build("drive", "v3", credentials=creds)

        # pylint: disable=maybe-no-member
        response = (
            service.files()
            .list(
                spaces="appDataFolder",
                fields="nextPageToken, files(id, name)",
                pageSize=10,
            )
            .execute()
        )
        for file in response.get("files", []):
            # Process change
            print(f'Found file: {file.get("name")}, {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        response = None

    return response.get("files")


def get_file(file_id):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)

    creds = creds["message"]

    try:
        # call drive api client
        service = build("drive", "v3", credentials=creds)

        # pylint: disable=maybe-no-member
        response = (
            service.files()
            .get( fileId=file_id)
            .execute()
        )
        print(response.items())
        print(dir(response))
        for file in response.get("files", []):
            # Process change
            print(f'Found file: {file.get("name")}, {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        response = None

    return response.get("files")



def save_file_to_drive(file_name, file_content):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)

    creds = creds["message"]

    try:
        # call drive api client
        service = build("drive", "v3", credentials=creds)

        # pylint: disable=maybe-no-member
        file_metadata = {
            'name': file_name,
            'parents': ['appDataFolder']  # Specify that the file should be saved in the App Folder.
        }

        # Create a BytesIO object for the file content
        file_stream = io.BytesIO(file_content.encode('utf-8'))

        # Create a media file upload object using the BytesIO stream
        media = MediaIoBaseUpload(file_stream, mimetype='text/plain')
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("id")


if __name__ == "__main__":
    os.chdir("../config")
    os.environ["CONFIG_PATH"] = os.getcwd()

    # Example usage - replace 'example.txt' and 'This is the content of the file.' with actual file name and content.
    #confirmation = save_file_to_drive("example.txt", "This is the content of the file.")
    #print(confirmation)
    get_file('1ZmDfZTvEn8chQLuhQy9shn06WGjVBYyOodzl6PU0cK8TOtdLkA')