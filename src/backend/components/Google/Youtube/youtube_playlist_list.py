import json
import os.path
from components.Google.google_credentials_create import createGoogleCredentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from components.utils.utils import set_config_path

ListYouTubePlaylists_description = {
    "type": "function",
    "function": {
        "name": "list_youtube_playlists",
        "description": "List all playlists from a specified YouTube channel. "
                       "Returns an array of playlist objects, each containing 'title' (string) and 'id' (string).",
        "parameters": {
            "type": "object",
            "properties": {
                "channelId": {
                    "type": "string",
                    "description": "The ID of the YouTube channel for which to list playlists."
                },
            },
            "required": ["channelId"]
        },
    }
}

def parseLocalPlaylist(playlist):
    return {
        "title": playlist.get("snippet").get("title"),
        "id": playlist.get("id"),
    }

def list_youtube_playlists(channelId):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]

    try:
        service = build("youtube", "v3", credentials=creds)

        playlists_response = service.playlists().list(
            part="snippet",
            channelId=channelId,
            maxResults=50
        ).execute()

        parsedPlaylists = [parseLocalPlaylist(playlist) for playlist in playlists_response.get("items", [])]
        return json.dumps(parsedPlaylists)
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    set_config_path()

    playlists = list_youtube_playlists("UCBGTgJyeNHWIaMcTdrveIGA")
    print(playlists)