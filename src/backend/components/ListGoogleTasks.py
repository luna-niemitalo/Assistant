import json
import os.path
from src.backend.components.CreateGoogleCredentials import createGoogleCredentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else :
        creds = creds["message"]

    try:
        service = build("tasks", "v1", credentials=creds)


        taskLists = json.load(open(os.path.join(os.environ["CONFIG_PATH"], "taskIDs.json")))

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
    os.chdir("../config")
    os.environ["CONFIG_PATH"] = os.getcwd()
    tasks = list_google_task("High")
    print(tasks)
