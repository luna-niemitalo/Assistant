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

    # Join with "config" to set the full config path
    config_path = os.path.join(cwd, "config")

    # Set the environment variable
    os.environ["CONFIG_PATH"] = config_path

    print(f"CONFIG_PATH has been set to: {config_path}")


from datetime import datetime

def verify_property(data, property_name):
    if data is None: return None
    if property_name in data:  # Check if property_name exists in data dictionary
        if data[property_name]:  # Check if property_name value is not None to avoid TypeError
            return data[property_name]
    return None

def build_db_message(data):
    content = verify_property(data, 'content')
    channel_id = verify_property(data, 'channel_id')
    guild_id = verify_property(data, 'guild_id')
    user_id = verify_property(verify_property(data, 'author'), 'id')
    timestamp = verify_property(data, 'timestamp')
    embeds = verify_property(data, 'embeds')
    components = verify_property(data, 'components')
    attachments = verify_property(data, 'attachments')
    mentions = verify_property(verify_property(data, 'mentions'), 'users')
    message_id = verify_property(data, 'id')

    referenced_message_id = None
    referenced_message = verify_property(data, 'referenced_message')
    if referenced_message:
        referenced_message_id = verify_property(referenced_message, 'id')



    #TODO handle timestamp to unix timestamp
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    unix_ts = int(dt.timestamp())
    result = {
        'content': content,
        'channel_id': channel_id,
        'guild_id': guild_id,
        'user_id': user_id,
        'timestamp': unix_ts,
        'embeds': embeds,
        'components': components,
        'attachments': attachments,
        'mentions': mentions,
        'reference': referenced_message_id,
        'id': message_id

    }

    return result
