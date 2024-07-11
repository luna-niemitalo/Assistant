import json
import os.path
import pickle
import quopri
from openai import OpenAI

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/tasks"]

CreateGoogleTask_description = {
    "type": "function",
    "function": {
        "name": "create_google_task",
        "description": "Create a task in Google Tasks with a specific importance level, and description, if tasks ",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the task, e.g., 'Buy groceries'"
                },
                "importance": {
                    "type": "string",
                    "enum": ["High", "Medium", "Low"],
                    "description": "The importance level of the task, e.g., 'High'"
                },
                "description": {
                    "type": "string",
                    "description": "The description of the task, e.g., 'Buy eggs, milk, and bread'"
                },
                "subtasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the subtask, e.g., 'Buy eggs'"
                            },
                            "description": {
                                "type": "string",
                                "description": "The description of the subtask, e.g., 'Free range, organic eggs'"
                            }
                        }
                    }
                }
            },
            "required": ["title", "importance", "description"]
        }
    }
}


def create_google_task(title, importance, description, subtasks = []):
    print("parameters", title, importance, description, subtasks)
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("tasks", "v1", credentials=creds)


        taskLists = json.load(open("taskIDs.json"))


        localTask = {
            "title": title,
            "notes": description,
        }
        result = service.tasks().insert(tasklist=taskLists[importance], body=localTask).execute()
        if subtasks:
            for subtask in subtasks:
                localTask = {
                    "title": subtask["title"],
                    "notes": subtask["description"],
                }
                service.tasks().insert(tasklist=taskLists[importance], body=localTask, parent=result["id"]).execute()
        return f"Task created: {result.get('title')}"
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    task = {
        "title": "Buy groceries",
        "importance": "High",
        "description": "Buy eggs, milk, and bread"
    }
    create_google_task(task["title"], task["importance"], task["description"], [{"title": "Buy eggs", "description": "Free range, organic eggs"}, {"title": "Buy milk", "description": "Whole milk"}, {"title": "Buy bread", "description": "Whole wheat bread"}])