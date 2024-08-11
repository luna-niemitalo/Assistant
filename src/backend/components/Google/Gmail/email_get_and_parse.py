import json
import os.path
from src.backend.components.Google.google_credentials_create import createGoogleCredentials
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
import re

from src.backend.components.utils.utils import set_config_path

# Function description structure
ParseEmail_description = {
    "type": "function",
    "function": {
        "name": "parse_email",
        "description": "Fetch and parse an email from Gmail by its ID. "
                       "Returns the subject and HTML content of the email.",
        "parameters": {
            "type": "object",
            "properties": {
                "emailId": {
                    "type": "string",
                    "description": "The ID of the email to be fetched and parsed."
                },
            },
            "required": ["emailId"]
        },
    },
}
def prune_string(input_str):
    # Define a regex pattern to keep alphanumeric characters, spaces, and some punctuation
    cleaned_str = re.sub(r'[^a-zA-Z0-9 äÄöÖåÅ,.:;?!\'"-]', '', input_str)

    # Optionally, also replace multiple spaces with a single space
    cleaned_str = re.sub(r'\s+', ' ', cleaned_str).strip()

    return cleaned_str

def parse_part(part):
    try:
        data = part['body']['data']
        mime_type = part['mimeType']
        print(mime_type)
        # If it is HTML content
        if mime_type == 'text/html':
            # Decode the data
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
            # Use BeautifulSoup to parse HTML
            soup = BeautifulSoup(decoded_data, 'html.parser')
            body_content = soup.get_text()  # Get plain text from HTML
            print(prune_string(body_content))
            return prune_string(body_content)
    except BaseException as error:
        return f"An error occurred while processing the email part: {error}"
def parse_email(emailId):
    creds = createGoogleCredentials()
    if creds["status"] == "error":
        return json.dumps(creds)
    else:
        creds = creds["message"]

    try:
        service = build("gmail", "v1", credentials=creds)

        # Fetching the email by ID
        email = service.users().messages().get(userId='me', id=emailId, format='full').execute()
        payload = email['payload']
        headers = payload['headers']

        # Extracting the subject from the headers
        subject = next((item['value'] for item in headers if item['name'] == 'Subject'), "No Subject")
        print(payload)
        # Getting the body content
        if 'body' in payload:
            content = parse_part(payload)
            if content:
                return json.dumps({"subject": subject, "content": content})

        results = []
        if 'parts' in payload:
            for part in payload['parts']:
                content = parse_part(part)
                if content:
                    results.append(content)
        if results:
            return json.dumps({"subject": subject, "content": " ".join(results)})
        return json.dumps({"subject": subject, "content": "No content found"})

    except HttpError as err:
        print(err)
        return json.dumps({"subject": "[ERROR]", "content": err})

if __name__ == "__main__":
    set_config_path()

    # Example usage with an email ID
    email_id = "190bf8b6fe4a2ba8"
    result = parse_email(email_id)
    print(result)