import json
import os
from typing import List, Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# scope_mappings.py
SCOPE_MAPPINGS = {
    "gmail.readonly": "https://www.googleapis.com/auth/gmail.readonly",
    "tasks": "https://www.googleapis.com/auth/tasks",
    "drive.readonly": "https://www.googleapis.com/auth/drive",
    "calendar": "https://www.googleapis.com/auth/calendar",
    "youtube": "https://www.googleapis.com/auth/youtube",
    # Add more mappings as needed
}


class CredentialsManager:
    def __init__(self, config_path: str = "./.accounts.json"):
        self.config_path = config_path
        self.accounts = self._load_accounts()
        self.client_secrets_file = None

    def _load_accounts(self) -> List[Dict]:
        """Load account configurations from the filesystem."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                return json.load(file)
        return []

    def save_config(self):
        """Save the current account configurations to the filesystem."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, ensure_ascii=False, indent=4)

    def set_scopes(self, account_name: str, scopes: List[str]):
        """Set the scopes for an account, delete token if present, and re-run auth flow."""
        # Check if account already exists
        for account in self.accounts:
            if account['account_name'] == account_name:
                if 'scopes' in account:
                    # Delete existing token file if scopes are being updated
                    token_path = f"{account_name}.json"
                    if os.path.exists(token_path):
                        os.remove(token_path)
                # Update scopes and re-run auth flow
                account['scopes'] = scopes
                self.save_config()
                self.run_auth_flow(account_name)
                return
        return "Account not found."

    def create_account(self, account_name: str, scopes: List[str] = None):
        if scopes is None:
            scopes = SCOPE_MAPPINGS.keys()

        # Add new account if not found and set scopes
        self.accounts.append({
            'account_name': account_name,
            'scopes': scopes
        })
        self.save_config()
        self.run_auth_flow(account_name)

    def run_auth_flow(self, account_name: str):
        """Re-run the OAuth flow and save a new token file for the account."""
        # Find the account and map its scope keys to URLs
        account = next((acc for acc in self.accounts if acc['account_name'] == account_name), None)
        if not account:
            raise ValueError("Account does not exist. Use set_scopes first.")

        scopes = [SCOPE_MAPPINGS[scope] for scope in account['scopes'] if scope in SCOPE_MAPPINGS]

        # Run OAuth flow to get credentials
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)

        # Save the token to a file named after the account
        token_path = f"{account_name}.json"
        with open(token_path, 'w') as token_file:
            token_file.write(credentials.to_json())

    def get_token(self, account_name: str) -> str:
        """Return a valid token for the specified account, refreshing if necessary."""
        account = next((acc for acc in self.accounts if acc['account_name'] == account_name), None)
        if not account:
            raise ValueError("Account not found.")

        token_path = f"{account_name}.json"
        credentials = None

        # Load credentials if they exist
        if os.path.exists(token_path):
            credentials = Credentials.from_authorized_user_file(token_path)

        # Validate token, refresh if expired
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except:
                    raise ValueError("Failed to refresh token. Rerun the auth flow.")
            else:
                # If token is invalid, rerun the auth flow
                raise ValueError("Token is invalid. Use rerun_auth_flow to reauthenticate.")

        return credentials.token
