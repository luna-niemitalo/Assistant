import json
import os.path
from src.backend.components.Google.google_credentials_create import createGoogleCredentials
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.backend.components.utils.utils import set_config_path

ListGmailEmails_description = {
    "type": "function",
    "function": {
        "name": "list_gmail_emails",
        "description": "Retrieve a list of emails from your Gmail account.",
        "parameters": {
            "type": "object",
            "properties": {
                "maxResults": {
                    "type": "integer",
                    "description": "The maximum number of emails to retrieve."
                },
                "query": {
                    "type": "string",
                    "description": "Gmail search query parameters (e.g., 'after:2024/7/7 before:2024/7/14')."
                }
            },
            "required": []
        },
    },
}

def prune_string(input_str):
    # Define a regex pattern to keep alphanumeric characters, spaces, and some punctuation
    cleaned_str = re.sub(r'[^a-zA-Z0-9 äÄöÖåÅ,.:;?!\'"-]', '', input_str)

    # Optionally, also replace multiple spaces with a single space
    cleaned_str = re.sub(r'\s+', ' ', cleaned_str).strip()

    return cleaned_str

def list_gmail_emails(maxResults=10, query=None):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]

    try:
        service = build("gmail", "v1", credentials=creds)

        # Call Gmail API to fetch emails with optional query
        if query:
            results = service.users().messages().list(userId='me', maxResults=maxResults, q=query).execute()
        else:
            results = service.users().messages().list(userId='me', maxResults=maxResults).execute()

        messages = results.get('messages', [])

        email_list = []
        if not messages:
            return json.dumps({"message": "No emails found."})
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], fields="id, internalDate, snippet, payload/headers").execute()
                result = prune_string(msg['snippet'])
                email_list.append({
                    "id": msg['id'],
                    "subject": next((item['value'] for item in msg['payload']['headers'] if item['name'] == 'Subject'), "No Subject"),
                    "snippet": result,
                    "date": msg['internalDate']  # Assuming the first header is the date
                })

        return json.dumps(email_list, indent=4)

    except HttpError as err:
        return json.dumps({"error": str(err)})

if __name__ == "__main__":
    set_config_path()

    # Example usage with a query
    result = list_gmail_emails(maxResults=5, query="after:2024/7/7 before:2024/7/14")
    print(result)