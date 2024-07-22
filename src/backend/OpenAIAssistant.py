import base64
import io

from openai import AssistantEventHandler
from FrontEndMessage import FrontEndMessage
from components.GetRainProbability import *
from components.CreateGoogleTask import *
from components.GetCurrentTemperature import *
from components.ListGoogleTasks import *
from components.CreateGoogleCalendarEvent import *
from components.GetTimeAndDate import *


def create_openai_assistant(self):
    self.assistant = self.client.beta.assistants.create(
        name="General Assistant for creating events, tasks, and parsing data",
        instructions="""
                You are a personal assistant. 
                Use provided information and functions to create events, tasks, and parse data
                Use markdown to format your text
            """,
        tools=[
            GetRainProbability_description,
            GetCurrentTemperature_description,
            CreateGoogleTask_description,
            ListGoogleTasks_description,
            CreateGoogleCalendarEvent_description,
            GetCurrentTimeAndDate_description
        ],
        model="gpt-4o" if self.selected_assistant == "OpenAI_4o" else "gpt-3.5-turbo-0125",
    )


def create_openai_thread(self):
    self.thread = self.client.beta.threads.create()
    self.thread_id = self.thread.id
    self.message_objects = [self.client.beta.threads.messages.create(
        thread_id=self.thread_id,
        role="assistant",
        content="Hello, how can I help you today?"
    )]


def upload_openai_file(self, file):
    base64_string = file['data']
    # Remove the data:image/png;base64, part if it exists
    if base64_string.startswith('data:image/png;base64,'):
        base64_string = base64_string.split(',')[1]

    # Decode the base64 string
    binary_data = base64.b64decode(base64_string)

    # Create a file-like object from the binary data
    file_like_object = io.BytesIO(binary_data)
    file_like_object.name = 'image.png'  # Important to set a name attribute with the correct extension

    openai_file_ref = self.client.files.create(file=file_like_object, purpose="vision")
    print(openai_file_ref)
    return openai_file_ref


def build_openai_message(self, message: FrontEndMessage):
    result = {
        'role': message.role,
        'content': []
    }
    if message.text:
        result['content'].append({"type": "text", "text": message.text})
    for item in message.images:
        file_ref = upload_openai_file(self, item)
        result['content'].append({"type": "image_file", "image_file": {"file_id": file_ref.id}})
    return result


def deconstruct_openai_message(message):
    mid = message.id
    text = ""
    for item in message.content:
        if item.type == "text":
            text += item.text.value + "\n"
    # text = message['content'][0]['text']['value']
    images = []
    for item in message.content:
        if item.type == "image_file":
            images.append(json.loads(item.image_file.to_json()))
    role = message.role
    timestamp = message.created_at
    result = FrontEndMessage(id=mid, text=text, images=images, role=role, timestamp=timestamp)
    return result


class OpenAI_AssistantEventHandler(AssistantEventHandler):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant

    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            self.handle_requires_action(event.data)
        elif event.event == 'thread.message.completed':
            # Find the message with the matching ID and update its content
            for message in self.assistant.message_objects:
                if message.id == event.data.id:
                    message.content = event.data.content
                    break
        elif event.event == "thread.message.delta":
            new_message = {
                "id": event.data.id,
                "content": json.loads(event.data.delta.to_json())["content"],
            }
            self.assistant.streamingMessage.put(new_message)
        elif event.event == "thread.message.created":
            self.assistant.message_objects.append(event.data)

    def handle_requires_action(self, data):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            json_args = json.loads(tool.function.arguments)
            function_name = tool.function.name
            if function_name in globals():
                function = globals()[function_name]
                result = function(**json_args)
                tool_outputs.append({"tool_call_id": tool.id, "output": result})
            else:
                print("Function not found")
                print(function_name)
                print(json_args)
                tool_outputs.append({"tool_call_id": tool.id, "output": "Function not found"})
        self.submit_tool_outputs(tool_outputs)

    def submit_tool_outputs(self, tool_outputs):
        new_event_handler = OpenAI_AssistantEventHandler(self)  # Create a new instance of the event handler

        with self.assistant.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=OpenAI_AssistantEventHandler(self.assistant),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()
