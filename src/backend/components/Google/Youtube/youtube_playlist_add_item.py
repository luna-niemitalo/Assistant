import json
import os.path
from src.backend.components.Google.google_credentials_create import createGoogleCredentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.backend.components.utils.utils import set_config_path

AddToYouTubePlaylist_description = {
    "type": "function",
    "function": {
        "name": "add_to_youtube_playlist",
        "description": "Add a video to a specified YouTube playlist by using the video ID. "
                       "Returns the updated playlist item object.",
        "parameters": {
            "type": "object",
            "properties": {
                "playlistId": {
                    "type": "string",
                    "description": "The ID of the YouTube playlist to which the video will be added."
                },
                "videoId": {
                    "type": "string",
                    "description": "The ID of the video to be added to the playlist."
                },
            },
            "required": ["playlistId", "videoId"]
        },
    },
}

def add_to_youtube_playlist(playlistId, videoId):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]

    try:
        service = build("youtube", "v3", credentials=creds)

        # Creating a request to add a video to the playlist
        request_body = {
            "snippet": {
                "playlistId": playlistId,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": videoId
                }
            }
        }

        response = service.playlistItems().insert(
            part="snippet",
            body=request_body
        ).execute()

        return json.dumps(response)

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    set_config_path()

    # Example usage
    result = add_to_youtube_playlist("YOUR_PLAYLIST_ID", "YOUR_VIDEO_ID")
    print(result)
