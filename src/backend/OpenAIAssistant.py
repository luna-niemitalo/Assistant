import base64
import io
import json

from openai import AssistantEventHandler
from FrontEndMessage import FrontEndMessage
from components.CreateGoogleTask import *
from components.ListGoogleTasks import *
from components.CreateGoogleCalendarEvent import *
from components.GetTimeAndDate import *
from components.ListGoogleCalendarEvents import *
from components.ParseWebsite import *
from components.ListYoutubePlaylists import *
from components.CreateYoutubePlaylist import *
from components.AddItemToYoutubePlaylist import *
from components.SearchYoutubeVideo import *
from components.GetAndParseEmail import *
from components.ListGoogleEmails import *
from components.SaveImportantInfo import *
from components.GoogleSearch import *
from src.backend.components.SaveImportantInfo import load_user_info

entries = []

def save_entry(parameter):
    """Saves the parameter and the current timestamp to the entries list."""
    timestamped_entry = {
        'parameter': parameter,
        'timestamp': datetime.now().isoformat()
    }
    entries.append(timestamped_entry)
    print(f"Saved entry: {timestamped_entry}")

def save_to_json_file(filename):
    """Saves the entries list to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(entries, file, indent=4)
    print(f"Saved entries to {filename}")

def replay_from_json_file(filename):
    """Reads from a JSON file and replays the saved entries."""
    global entries
    with open(filename, 'r') as file:
        entries = json.load(file)
        for entry in entries:
            print(f"Parameter: {entry['parameter']}, Timestamp: {entry['timestamp']}")
def create_openai_assistant(self):
    user_info = load_user_info()
    instructions = f"""
                You are a personal assistant.
                

                Immediate Recognition: As soon as user mentions a new person, event, artist, topic, or any interest, You'll recognize it as potential information to save.
            
                Instant Action: You will immediately use the save information tool to record this new interest or preference without delaying it until the end of the task or conversation.
            
                Verification: I will confirm with you that the information has been saved correctly, ensuring transparency and accuracy.

                Greet the user politely and ask how you can help them.
                
                Use provided information and tools to fullill the user's requests.
                
                For example by listing and reminding about tasks to be done, or providing information about the day's schedule.
                
                Use markdown to format your text except when managing google tools, for google tools write the description using HTML and be verbose, and include as much information as possible, and make it look neat and readable 
            """
    instructions += "USER INFORMATION: " + json.dumps(user_info, indent=4)
    try:
        self.assistant = self.client.beta.assistants.create(
            name="General Assistant for creating events, tasks, and parsing data",
            instructions=instructions,
            tools=[
                CreateGoogleTask_description,
                ListGoogleTasks_description,
                CreateGoogleCalendarEvent_description,
                GetCurrentTimeAndDate_description,
                GetGoogleCalendarEvents_description,
                ParseWebsite_description,
                ListYouTubePlaylists_description,
                CreateYouTubePlaylist_description,
                AddToYouTubePlaylist_description,
                SearchYouTube_description,
                ParseEmail_description,
                ListGmailEmails_description,
                SaveANoteAboutUser,
                UpdateUserInformation_description,
                GooogleSearch_description
            ],
            model="gpt-4o" if self.selected_assistant == "OpenAI_4o" else "gpt-4o-mini",
        )
    except Exception as e:
        self.assistant.status_messages.append({
            "timestamp": datetime.now().timestamp(),
            "message": f"Error creating assistant: {e}"
        })
        return None


def create_openai_thread(self):
    self.thread = self.client.beta.threads.create()
    self.thread_id = self.thread.id
    self.status_messages = []
    self.message_objects = []


def upload_openai_file(self, file):
    base64_string = file['data']
    # Remove the data:image/png;base64, part if it exists
    extension = base64_string.split(';')[0].split('/')[1]
    base64_string = base64_string.split(',')[1]

    # Decode the base64 string
    binary_data = base64.b64decode(base64_string)

    # Create a file-like object from the binary data
    file_like_object = io.BytesIO(binary_data)
    file_like_object.name = 'image.' + extension  # Important to set a name attribute with the correct extension

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


def handleStreamingAudio(audio):
    audio_data = base64.b64decode(audio)
    with open("audio.wav", "wb") as f:
        f.write(audio_data)
    return "Audio received"

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
                    self.assistant.set_force_update()
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
                self.assistant.status_messages.append({
                    "timestamp": datetime.now().timestamp(),
                    "message": f"[EVENT] Running {function_name} with arguments: {json_args}"
                })
                function = globals()[function_name]
                result = function(**json_args)
                self.assistant.status_messages.append({
                    "timestamp": datetime.now().timestamp(),
                    "message": f"[EVENT] {function_name} returned: {result}"
                })
                if not result:
                    result = "Function returned None"
                tool_outputs.append({"tool_call_id": tool.id, "output": result})
            else:
                print("Function not found")
                print(function_name)
                print(json_args)
                tool_outputs.append({"tool_call_id": tool.id, "output": "Function not found"})
        self.submit_tool_outputs(tool_outputs)

    def submit_tool_outputs(self, tool_outputs):

        with self.assistant.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=OpenAI_AssistantEventHandler(self.assistant),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()

    def streamAudio(self):
        response = self.assistant.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input="Hello world! This is a streaming test.",
            response_format="opus",
        )

        response.stream_to_file("output.mp3")