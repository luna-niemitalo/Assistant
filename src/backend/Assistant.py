import json
import os

from FrontEndMessage import FrontEndMessage
from OpenAIAssistant import create_openai_assistant, create_openai_thread, OpenAI_AssistantEventHandler, \
    build_openai_message, deconstruct_openai_message
from openai import OpenAI
import queue


class Assistant:
    selected_assistant = ""
    message_objects = []
    streamingMessage = queue.Queue()

    def __init__(self, assistant):
        self.thread_id = None
        self.thread = None
        self.assistant = None
        self.selected_assistant = assistant
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            self.event_handler = OpenAI_AssistantEventHandler(self)
            token = json.load(open(os.environ["CONFIG_PATH"] + "/OpenAI_token.json"))
            self.client = OpenAI(
                organization=token["organization"],
                api_key=token["api_key"],
                project=token["project"],
            )
            create_openai_thread(self)
            create_openai_assistant(self)

    def add_message(self, message: FrontEndMessage):
        result = None
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            oai_content = build_openai_message(self, message)
            oai_message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role=message.role,
                content=oai_content['content']
            )
            self.message_objects.append(oai_message)
            print("Message created: ", oai_message)
            result = deconstruct_openai_message(oai_message)
            print("Result: ", result.get_fem())

        self.run_ai()
        return result

    def get_messages(self):
        results = []
        for message in self.message_objects:
            if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
                fe_message = deconstruct_openai_message(message)
                results.append(fe_message)

        return results

    def new_thread(self):
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            create_openai_thread(self)
            return self.thread_id

    def run_ai(self):
        print("Running AI")
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            new_event_handler = OpenAI_AssistantEventHandler(self)  # Create a new instance of the event handler
            with self.client.beta.threads.runs.stream(
                    thread_id=self.thread_id,
                    assistant_id=self.assistant.id,
                    event_handler=new_event_handler
            ) as stream:
                stream.until_done()
