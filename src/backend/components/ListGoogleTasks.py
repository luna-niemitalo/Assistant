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

ListGoogleTasks_description = {
    "type": "function",
    "function": {
        "name": "list_google_task",
        "description": "List all tasks in Google Tasks with a specific (optional)importance level,  "
                       "Returns an array of task objects, each containing 'title' (string), importance (enum: 'High' | 'Medium' | 'Low') and 'description' (string).",
        "parameters": {
            "type": "object",
            "properties": {
                "importance": {
                    "type": "string",
                    "enum": ["High", "Medium", "Low"],
                    "description": "The importance level of the task, e.g., 'High'"
                },
            },
            "required": []
        },
    }
}

def parseLocalTask(googleTask, list):
    return {
        "title": googleTask.get("title"),
        "importance": list,
        "description": googleTask.get("notes"),
    }


def list_google_task(importance = "all"):
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("../token.json"):
        creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("../token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("tasks", "v1", credentials=creds)


        taskLists = json.load(open("../taskIDs.json"))

        if importance == "all":
            parsedTasks = []
            for key, value in taskLists.items():
                tasks = service.tasks().list(tasklist=taskLists[key]).execute()
                parsedTasks += [parseLocalTask(task, key) for task in tasks.get("items", [])]
            return json.dumps(parsedTasks)
        tasks = service.tasks().list(tasklist=taskLists[importance]).execute()
        parsedTasks = [parseLocalTask(task, importance) for task in tasks.get("items", [])]
        return json.dumps(parsedTasks)
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    tasks = list_google_task("High")
    print(tasks)
    #create_task(task)