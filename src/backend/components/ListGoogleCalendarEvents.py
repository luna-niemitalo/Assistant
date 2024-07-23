import json
import os.path
from datetime import datetime, timedelta
from src.backend.components.CreateGoogleCredentials import createGoogleCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

GetGoogleCalendarEvents_description = {
    "type": "function",
    "function": {
        "name": "get_google_calendar_events",
        "description": "Retrieve Google Calendar events within a specified time range, potential calendar id's are: 'luna.niemitalo@refined.com' for work, and 'jani.niemitalo@gmail.com' for personal",
        "parameters": {
            "type": "object",
            "properties": {
                "time_min": {
                    "type": "string",
                    "description": "The start time of the events in RFC3339 format (e.g., '2024-07-20T10:00:00-07:00')"
                },
                "time_max": {
                    "type": "string",
                    "description": "The end time of the events in RFC3339 format (e.g., '2024-07-27T10:00:00-07:00')"
                },
                "calendar_id": {
                    "type": "string",
                    "description": "The ID of the calendar to fetch events from"
                },
            },
            "required": ["calendar_id"]
        },
    }
}

def parse_google_calendar_events(event):
    result = {
        "summary": event["summary"],
        "location": event.get("location", ""),
        "description": event.get("description", ""),
    }
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    result["start"] = start
    result["end"] = end
    return result


def get_google_calendar_events(calendar_id, time_min=None, time_max=None):
    print("Fetching events for calendar:", calendar_id)

    # Default time range settings
    if not time_min:
        time_min = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    if not time_max:
        time_max = (datetime.utcnow() + timedelta(weeks=1)).isoformat() + 'Z'

    creds = createGoogleCredentials()

    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]

    try:
        service = build("calendar", "v3", credentials=creds)
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            )
            .execute()
        )
        events = events_result.get('items', [])

        if not events:
            print("No upcoming events found.")
            return json.dumps([])
        parsed = [parse_google_calendar_events(event) for event in events]
        return json.dumps(parsed)
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


if __name__ == "__main__":

    os.chdir("../config")
    os.environ["CONFIG_PATH"] = os.getcwd()
    event_list = get_google_calendar_events(
        calendar_id='luna.niemitalo@refined.com'
    )
    #print(event_list)