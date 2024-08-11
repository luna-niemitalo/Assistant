import json
import os.path
from src.backend.components.Google.google_credentials_create import createGoogleCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.backend.components.utils.utils import set_config_path

CreateGoogleCalendarEvent_description = {
    "type": "function",
    "function": {
        "name": "create_google_calendar_event",
        "description": "Create a Google Calendar event with specified details",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "The summary or title of the event"
                },
                "location": {
                    "type": "string",
                    "description": "The location of the event"
                },
                "description": {
                    "type": "string",
                    "description": "HTML  formatted event description"
                },
                "start": {
                    "type": "string",
                    "description": "The start date and time of the event in RFC3339 format (e.g., '2024-07-20T10:00:00-07:00')"
                },
                "end": {
                    "type": "string",
                    "description": "The end date and time of the event in RFC3339 format (e.g., '2024-07-20T11:00:00-07:00')"
                },
            },
            "required": ["summary", "start", "end"]
        },
    }
}

def create_google_calendar_event(summary, start, end, location=None, description=None):
    print("parameters", summary, start, end, location, description)
    creds = createGoogleCredentials()

    if creds["status"] == "error":
        return json.dumps(creds)
    else :
        creds = creds["message"]

    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start,
                'timeZone': 'Europe/Helsinki',  # Adjust timeZone as needed
            },
            'end': {
                'dateTime': end,
                'timeZone': 'Europe/Helsinki',  # Adjust timeZone as needed
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        return json.dumps(event)
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


if __name__ == "__main__":
    set_config_path()
    event = create_google_calendar_event(
        summary="Sample Event",
        location="800 Howard St., San Francisco, CA 94103",
        description="A chance to hear more about Google's developer products.",
        start="2024-07-20T10:00:00-07:00",
        end="2024-07-20T11:00:00-07:00"
    )
    print(event)
