# app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import time
import os
import hashlib
import json
import queue
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

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



with open(os.environ["CONFIG_PATH"] + "/OpenAI_token.json") as f:
    token = json.load(f)

client = OpenAI(
    organization=token["organization"],
    api_key=token["api_key"],
    project=token["project"],
)

thread = client.beta.threads.create()
thread_id = thread.id

streamingMessage = queue.Queue()

app = Flask(__name__)
CORS(app)
assistant = client.beta.assistants.create(
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
    model="gpt-3.5-turbo-0125",
)

message_objects = [
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="assistant",
        content="Hello, how can I help you today?",
    ),
]

def message_to_json(message):
    return json.loads(message.to_json())



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
            if len(message_objects) != prev_length:
                yield f"data: {json.dumps([message_to_json(message) for message in message_objects])}\n\n"
                prev_length = len(message_objects)
            time.sleep(0.1)
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/api/message/stream', methods=['GET'])
def message_stream():
    def event_stream():
        while True:
            if not streamingMessage.empty():
                message = streamingMessage.get()
                yield f"data: {json.dumps(message)}\n\n"
            else:
                time.sleep(0.3)
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/api/message', methods=['POST'])
def add_message():
    jsonMessage = request.get_json()
    print(jsonMessage["content"][1])
    newMessage = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=jsonMessage["role"],
        content=jsonMessage["content"],
    )
    client.beta.threads.messages.create()
    message_objects.append(newMessage)
    #run_ai()
    return newMessage.to_json()

@app.route('/api/thread/id', methods=['GET'])
def messages_thread_id():
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
    global thread_id, thread
    thread = client.beta.threads.create()
    thread_id = thread.id
    message_objects.clear()
    message_objects.append(client.beta.threads.messages.create(
        thread_id=thread_id,
        role="assistant",
        content="Hello, how can I help you today?",
    ))
    return thread_id


class EventHandler(AssistantEventHandler):
    @override
    def on_event(self, event):
        #print(event.data)
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)
        elif event.event == 'thread.message.completed':
            # Find the message with the matching ID and update its content
            for message in message_objects:
                if message.id == event.data.id:
                    message.content = event.data.content
                    break
        elif event.event == "thread.message.delta":
            new_message = {
                "id": event.data.id,
                "content": json.loads(event.data.delta.to_json())["content"],
            }
            streamingMessage.put(new_message)
        elif event.event == "thread.message.created":
            message_objects.append(event.data)

    def handle_requires_action(self, data, run_id):
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
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()

def run_ai():
    print("Running AI")
    with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant.id,
            event_handler=EventHandler()
    ) as stream:
        stream.until_done()


if __name__ == '__main__':
    app.run(debug=True)
