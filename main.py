import gradio as gr
import json
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

from GetRainProbability import GetRainProbability_description, get_rain_probability
from GetCurrentTemperature import GetCurrentTemperature_description, get_current_temperature
from CreateGoogleTask import CreateGoogleTask_description, create_google_task
from ListGoogleTasks import ListGoogleTasks_description, list_google_task

# Load OpenAI_token.json file to get the API key
with open("OpenAI_token.json") as f:
    token = json.load(f)

client = OpenAI(
    organization=token["organization"],
    api_key=token["api_key"],
    project=token["project"],
)

assistant = client.beta.assistants.create(
    name="General Assistant for creating events, tasks, and parsing data",
    instructions="You are a personal assistant. Use provided information and functions to create events, tasks, and parse data. if there is an error just report it and don't try to recall the function.",
    tools=[GetRainProbability_description, GetCurrentTemperature_description, CreateGoogleTask_description, ListGoogleTasks_description],
    model="gpt-3.5-turbo-0125",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What tasks do i have coming up?",
)


class EventHandler(AssistantEventHandler):
    @override
    def on_event(self, event):
        # Retrieve events that are denoted with 'requires_action'
        # since these will have our tool_calls
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id  # Retrieve the run ID from the event data
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            jsonArgs = json.loads(tool.function.arguments)
            function_name = tool.function.name
            # Check if the function exists in the global scope
            if function_name in globals():
                # Get the function from the global scope
                function = globals()[function_name]

                # Call the function with the arguments
                result = function(**jsonArgs)
                tool_outputs.append({"tool_call_id": tool.id, "output": result})
            else:
                print("Function not found")
                print(function_name)
                print(jsonArgs)
                tool_outputs.append({"tool_call_id": tool.id, "output": "Function not found"})

        # Submit all tool_outputs at the same time
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        # Use the submit_tool_outputs_stream helper
        with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()


with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler()
) as stream:
    stream.until_done()
