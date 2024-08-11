import json
from datetime import datetime
import pytz
import os


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


def load_user_info():
    file_path = os.path.join(os.environ["CONFIG_PATH"], 'user_information', 'user_information.md')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    else:
        return "Unable to load user information. Please ensure the file exists at 'config/user_information/user_information.md'."



def set_config_path():
    # Get the current working directory
    cwd = os.getcwd()

    # Find the base path "src\backend"
    backend_index = cwd.find("src\\backend")

    if backend_index == -1:
        print("The path 'src\\backend' was not found in the current working directory.")
        return

    # Get the path up to "src\backend"
    base_path = cwd[:backend_index + len("src\\backend")]

    # Join with "config" to set the full config path
    config_path = os.path.join(base_path, "config")

    # Set the environment variable
    os.environ["CONFIG_PATH"] = config_path

    print(f"CONFIG_PATH has been set to: {config_path}")
