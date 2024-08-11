import json
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.backend.components.Google.google_credentials_create import createGoogleCredentials
from src.backend.components.utils.utils import set_config_path

# If modifying these scopes, delete the file token.json.
CreateGoogleTask_description = {
    "type": "function",
    "function": {
        "name": "create_google_task",
        "description": "Create a task in Google Tasks with a specific importance level, and description",
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
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else :
        creds = creds["message"]

    try:
        service = build("tasks", "v1", credentials=creds)


        taskLists = json.load(open(os.path.join(os.environ["CONFIG_PATH"], "taskIDs.json")))


        localTask = {
            "title": title,
            "notes": description,
        }
        result = service.tasks().insert(tasklist=taskLists[importance], body=localTask).execute()
        if subtasks:
            for subtask in subtasks:
                localTask = {
                    "title": subtask["title"],
                    "notes": subtask["description"] if "description" in subtask else "",
                }
                service.tasks().insert(tasklist=taskLists[importance], body=localTask, parent=result["id"]).execute()
        return f"Task created: {result.get('title')}"
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    set_config_path()

    task = {
        "title": "Buy groceries",
        "importance": "High",
        "description": "Buy eggs, milk, and bread"
    }
    create_google_task(task["title"], task["importance"], task["description"], [{"title": "Buy eggs", "description": "Free range, organic eggs"}, {"title": "Buy milk", "description": "Whole milk"}, {"title": "Buy bread", "description": "Whole wheat bread"}])