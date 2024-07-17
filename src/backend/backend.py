# app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import time
import os
import hashlib
import json
import queue
import base64
from openai import OpenAI
from typing_extensions import override, Iterable
from openai import AssistantEventHandler
from typing import List, Union
import io

print(os.getcwd())
path = os.getcwd() + "/config"
os.environ["CONFIG_PATH"] = path

SCOPES = json.load(open(os.environ["CONFIG_PATH"] + "/scopes.json"))

from components.GetRainProbability import *
from components.CreateGoogleTask import *
from components.GetCurrentTemperature import *
from components.ListGoogleTasks import *
from components.CreateGoogleCalendarEvent import *
from components.GetTimeAndDate import *


assistant_options = ["OpenAI_4o", "OpenAI_3.5", "LLAMA3"]

class FrontEndMessage:
    def __init__(self, text, images, role, id = None, timestamp = None):
        self.id = id
        self.text = text
        self.images = images
        self.role = role
        self.timestamp = timestamp

    def get_fem(self):
        return {
            "id": self.id,
            "text": self.text,
            "images": self.images,
            "role": self.role,
            "timestamp": self.timestamp
        }


class Assistant(AssistantEventHandler):
    selected_assistant = ""
    message_objects = []
    streamingMessage = queue.Queue()


    def __init__(self, assistant):
        super().__init__()
        self.thread_id = None
        self.thread = None
        self.selected_assistant = assistant
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            token = json.load(open(os.environ["CONFIG_PATH"] + "/OpenAI_token.json"))
            self.client = OpenAI(
                organization=token["organization"],
                api_key=token["api_key"],
                project=token["project"],
            )
            self.create_openai_thread()
            self.create_openai_assistant()

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
        self.message_objects.clear()
        self.message_objects.append(self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="assistant",
            content="Hello, how can I help you today?"
        ))


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



    @override # This is OpenAI exclusive
    def on_event(self, event):
        # print(event.data)
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.OpenAI_handle_requires_action(event.data, run_id)
        elif event.event == 'thread.message.completed':
            # Find the message with the matching ID and update its content
            for message in self.message_objects:
                if message.id == event.data.id:
                    message.content = event.data.content
                    break
        elif event.event == "thread.message.delta":
            new_message = {
                "id": event.data.id,
                "content": json.loads(event.data.delta.to_json())["content"],
            }
            self.streamingMessage.put(new_message)
        elif event.event == "thread.message.created":
            self.message_objects.append(event.data)

    def OpenAI_handle_requires_action(self, data, run_id):
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            jsonArgs = json.loads(tool.function.arguments)
            function_name = tool.function.name
            if function_name in globals():
                function = globals()[function_name]
                result = function(**jsonArgs)
                tool_outputs.append({"tool_call_id": tool.id, "output": result})
            else:
                print("Function not found")
                print(function_name)
                print(jsonArgs)
                tool_outputs.append({"tool_call_id": tool.id, "output": "Function not found"})
        self.OpenAI_submit_tool_outputs(tool_outputs, run_id)

    def OpenAI_submit_tool_outputs(self, tool_outputs, run_id):
        with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=self,
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()

    def build_openai_message(self, message: FrontEndMessage):
        result = {
            'role': message.role,
            'content': []
        }
        if message.text:
            result['content'].append({"type": "text", "text": message.text})
        for item in message.images:
            file_ref = self.upload_openai_file(item)
            result['content'].append({"type": "image_file", "image_file": {"file_id": file_ref.id}})
        return result

    def deconstruct_openai_message(self, message):
        id = message.id
        text = ""
        for item in message.content:
            if item.type == "text":
                text += item.text.value + "\n"
        #text = message['content'][0]['text']['value']
        images = []
        for item in message.content:
            if item.type == "image_file":
                images.append(item.image_file.to_json())
        role = message.role
        timestamp = message.created_at
        result = FrontEndMessage(id=id, text=text, images=images, role=role, timestamp=timestamp)
        return result


    def add_message(self, message: FrontEndMessage):
        result = None
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            oai_content = self.build_openai_message(message)
            oai_message = self.client.beta.threads.messages.create(
                thread_id=self.thread_id,
                role=message.role,
                content=oai_content['content']
            )
            self.message_objects.append(oai_message)
            print("Message created: ", oai_message)
            result = self.deconstruct_openai_message(oai_message)
            print("Result: ", result.get_fem())

        self.run_ai()
        return result

    def get_messages(self):
        results = []
        for message in self.message_objects:
            if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
                fe_message = self.deconstruct_openai_message(message)
                results.append(fe_message)

        return results

    def new_thread(self):
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            self.create_openai_thread()
            return self.thread_id

    def run_ai(self):
        print("Running AI")
        if self.selected_assistant == "OpenAI_4o" or self.selected_assistant == "OpenAI_3.5":
            with self.client.beta.threads.runs.stream(
                    thread_id=self.thread_id,
                    assistant_id=self.assistant.id,
                    event_handler=self
            ) as stream:
                stream.until_done()



app = Flask(__name__)
CORS(app)


assistant = Assistant(assistant_options[0])


@app.route('/api/data', methods=['GET'])
def get_data():
    print("Getting data")
    data = {"message": "Hello from Flask!"}
    return jsonify(data)


@app.route('/api/messages', methods=['GET'])
def messages():
    def event_stream():

        prev_length = 0
        while True:
            fem = assistant.get_messages()
            if len(fem) != prev_length:
                print("Messages: ", fem)
                yield f"data: {json.dumps([message.get_fem() for message in fem])}\n\n"
                prev_length = len(fem)
            time.sleep(0.1)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/api/message/stream', methods=['GET'])
def message_stream():
    def event_stream():
        while True:
            if not assistant.streamingMessage.empty():
                print("Streaming message")
                message = assistant.streamingMessage.get()
                yield f"data: {json.dumps(message)}\n\n"
            else:
                time.sleep(0.3)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/api/message', methods=['POST'])
def add_message():
    jsonMessage = request.get_json(force=True)
    fem = FrontEndMessage(
        text=jsonMessage['text'],
        images=jsonMessage['images'],
        role=jsonMessage['role'],
    )
    result = assistant.add_message(fem)
    print("Result: ", result.get_fem())
    return json.dumps(result.get_fem())


@app.route('/api/thread/id', methods=['GET'])
def messages_thread_id():
    thread_id = assistant.thread_id
    print("Thread ID: ", thread_id)
    def event_stream():
        prev_thread_id = ""
        while True:
            if thread_id != prev_thread_id:
                yield f"data: {thread_id}\n\n"
                prev_thread_id = thread_id
            time.sleep(1)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/api/thread/new', methods=['POST'])
def new_thread():
    print("New thread")
    return assistant.new_thread()


if __name__ == '__main__':
    app.run(debug=True)
