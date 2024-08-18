import json
import os.path
from components.Google.google_credentials_create import createGoogleCredentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from components.utils.utils import set_config_path

SearchYouTube_description = {
    "type": "function",
    "function": {
        "name": "search_youtube_video",
        "description": "Search YouTube for videos based on a query string. "
                       "Returns a list of video objects, each containing ‘title’ (string), 'videoId' (string), and 'description' (string).",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for the video"
                },
                "maxResults": {
                    "type": "integer",
                    "description": "The maximum number of results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        },
    }
}

def parseYouTubeVideo(video):
    return {
        "title": video["snippet"]["title"],
        "videoId": video["id"]["videoId"],
        "description": video["snippet"]["description"],
    }

def search_youtube_video(query, maxResults=5):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]

    try:
        service = build("youtube", "v3", credentials=creds)

        request = service.search().list(
            part="snippet",
            q=query,
            maxResults=maxResults,
            type="video"
        )
        response = request.execute()
        print(response.get("items", []))

        parsedVideos = [parseYouTubeVideo(item) for item in response.get("items", [])]
        return json.dumps(parsedVideos)

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    set_config_path()

    videos = search_youtube_video("Python tutorial", maxResults=3)
    print(videos)
