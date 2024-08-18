import json
import os.path
from components.Google.google_credentials_create import createGoogleCredentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from components.utils.utils import set_config_path

CreateYouTubePlaylist_description = {
    "type": "function",
    "function": {
        "name": "create_youtube_playlist",
        "description": "Creates a new YouTube playlist with a specified title and description. "
                       "Returns a playlist object containing the playlist ID and title.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the playlist."
                },
                "description": {
                    "type": "string",
                    "description": "A description of the playlist."
                },
            },
            "required": ["title", "description"]
        },
    }
}

def create_youtube_playlist(title, description):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]

    try:
        # Build the YouTube service
        service = build("youtube", "v3", credentials=creds)

        # Create the playlist
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["youtube", "playlist"],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "unlisted"  # Options: public, unlisted, private
            }
        }

        request = service.playlists().insert(
            part="snippet,status",
            body=request_body
        )

        response = request.execute()
        return json.dumps({
            "id": response["id"],
            "title": response["snippet"]["title"]
        })
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    set_config_path()

    new_playlist = create_youtube_playlist("My Awesome Playlist", "A collection of my favorite videos.")
    print(new_playlist)