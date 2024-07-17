import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
                    "description": "A detailed description of the event"
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
    """Creates an event on the user's primary calendar."""
    SCOPES = json.load(open(os.environ["CONFIG_PATH"] + "/scopes.json"))

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.environ["CONFIG_PATH"] + "/token.json"):
        creds = Credentials.from_authorized_user_file(os.environ["CONFIG_PATH"] + "/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.environ["CONFIG_PATH"] + "/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.environ["CONFIG_PATH"] + "/token.json", "w") as token:
            token.write(creds.to_json())

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

    os.chdir("../config")
    os.environ["CONFIG_PATH"] = os.getcwd()
    event = create_google_calendar_event(
        summary="Sample Event",
        location="800 Howard St., San Francisco, CA 94103",
        description="A chance to hear more about Google's developer products.",
        start="2024-07-20T10:00:00-07:00",
        end="2024-07-20T11:00:00-07:00"
    )
    print(event)
