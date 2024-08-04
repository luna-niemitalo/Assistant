import json
import os
import re


SaveANoteAboutUser = {
    "type": "function",
    "function": {
        "name": "save_user_information",
        "description": "Append a note about important information about the user to learn about their preferences and details to the user information.",
        "parameters": {
            "type": "object",
            "properties": {
                "information": {
                    "type": "string",
                    "description": "Important information about the user (e.g., name, birthday, location, hobbies, preferences)."
                }
            },
            "required": ["information"]
        },
    }
}

UpdateUserInformation_description = {
    "type": "function",
    "function": {
        "name": "update_user_information",
        "description": "Updates specific information about the user by replacing the old information with new data. This helps keep user preferences and details accurate.",
        "parameters": {
            "type": "object",
            "properties": {
                "text_to_replace": {
                    "type": "string",
                    "description": "The EXACT string contained in the user information that you want to replace."
                },
                "replacement": {
                    "type": "string",
                    "description": "The new information that will replace the old information."
                }
            },
            "required": ["text_to_replace", "replacement"]
        }
    }
}

def update_user_information(text_to_replace: str, replacement: str):
    # Fetch the existing user information from the database or storage system
    user_data: str = load_user_info()

    # Replace the old information with new data
    try:
        res = re.compile(re.escape(text_to_replace), re.IGNORECASE)
        user_data = res.sub(replacement, user_data)
        # Save the updated user information back to the database or storage system
        save_user_info_to_file(user_data)
    except Exception as e:
        return "Update failed. Please check the input data and try again." + str(e)

    return user_data

def load_user_info():
    DATA_FILE = os.path.join(os.environ["CONFIG_PATH"], "user_info.txt")

    """Load user information from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return file.read()
    return ""

def save_user_info_to_file(data):
    DATA_FILE = os.path.join(os.environ["CONFIG_PATH"], "user_info.txt")

    """Save user information to the JSON file."""
    with open(DATA_FILE, 'w') as file:
        file.write(data)

def save_user_information(information):
    """Saves important information about the user."""
    user_data: str = load_user_info()
    user_data +=  "\n" + information
    save_user_info_to_file(user_data)

    return json.dumps({
        "status": "success",
        "message": "Information saved for the user.",
        "user_data": user_data
    })

if __name__ == "__main__":
    os.chdir("../config")
    os.environ["CONFIG_PATH"] = os.getcwd()
    # Example of usage
    user_info = {
        "name": "Luna",
        "Birthday": "26.1.1996",
        "Location": "Helsinki, Finland",
        "Hobbies": "Reading, coding, and playing video games"
    }
    current_status = save_user_information(user_info)
    print(current_status)