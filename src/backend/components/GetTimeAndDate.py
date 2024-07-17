import json
from datetime import datetime
import pytz

GetCurrentTimeAndDate_description = {
    "type": "function",
    "function": {
        "name": "get_current_time_and_date",
        "description": "Get the current date and time in a specified timezone",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "The timezone for which to get the current date and time (e.g., 'Europe/Helsinki')"
                },
            },
            "required": []
        },
    }
}

def get_current_time_and_date(timezone = "Europe/Helsinki"):
    print("getting current time and date")
    """Get the current date and time in a specified timezone."""
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return json.dumps({
            "date": current_time.strftime('%Y-%m-%d'),
            "time": current_time.strftime('%H:%M:%S'),
            "timezone": timezone
        })
    except pytz.UnknownTimeZoneError:
        return json.dumps({
            "error": f"Unknown timezone: {timezone}"
        })

if __name__ == "__main__":
    current_time = get_current_time_and_date("America/Los_Angeles")
    print(current_time)
