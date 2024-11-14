from GoogleCredentialsManager import CredentialsManager

class GoogleTools:
    def __init__(self):
        self.credentials_manager = CredentialsManager()
        self.tool_descriptions = []
        self.tools = []

    def register_tool(self, tool_description, tool_function):
        self.tool_descriptions.append(tool_description)
        self.tools.append(tool_function)

    def google_task_create(self, title, importance, description, subtasks=[]):

