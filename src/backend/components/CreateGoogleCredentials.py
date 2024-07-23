import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
def createGoogleCredentials():
    SCOPES = json.load(open(os.path.join(os.environ["CONFIG_PATH"], "scopes.json")))

    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(os.environ["CONFIG_PATH"], "token.json")):
        creds = Credentials.from_authorized_user_file(os.path.join(os.environ["CONFIG_PATH"], "token.json"), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(os.environ["CONFIG_PATH"] + "credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(os.environ["CONFIG_PATH"], "token.json"), "w") as token:
            token.write(creds.to_json())
    return {"status": "success", "message": creds}