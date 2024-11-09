# Assistant Application

This repository contains a personal assistant application built using Vue.js and a Python backend that handles various tasks and events, specifically tailored for user interaction with a chat interface and handling user created custom API tools, so the Assistant has access to data not normally available to assistants

## Features

- Real-time messaging system.
- Image handling within messages.
- Various assistant functionalities including task management and calendar events.
- Dynamic theme selection and assistant selection.

## Technologies Used

- **Frontend**: Vue.js, TypeScript, SCSS
- **Backend**: OpenAI API, Flask 
- **Others**: Markdown for message rendering, Highlight.js for syntax highlighting

## File Structure

* 
* ├── src
* │ ├── backend
* │ │ ├── components
* │ │ │ ├── AddItemToYoutubePlaylist.py
* │ │ │ ├── CreateGoogleCalendarEvent.py
* │ │ │ ├── CreateGoogleCredentials.py
* │ │ │ ├── CreateGoogleTask.py
* │ │ │ ├── CreateYoutubePlaylist.py
* │ │ │ ├── GetAndParseEmail.py
* │ │ │ ├── GetTimeAndDate.py
* │ │ │ ├── GoogleSearch.py
* │ │ │ ├── ListGoogleCalendarEvents.py
* │ │ │ ├── ListGoogleEmails.py
* │ │ │ ├── ListGoogleTasks.py
* │ │ │ ├── ListYoutubePlaylists.py
* │ │ │ ├── ParseWebsite.py
* │ │ │ ├── SaveImportantInfo.py
* │ │ │ └── SearchYoutubeVideo.py
* │ │ ├── config
* │ │ │ ├── credentials.json
* │ │ │ ├── OpenAI_token.json
* │ │ │ ├── scopes.json
* │ │ │ ├── taskIDs.json
* │ │ │ ├── token.json
* │ │ │ └── user_info.txt
* │ │ ├── Assistant.py
* │ │ ├── backend.py
* │ │ ├── entries.json
* │ │ ├── FrontEndMessage.py
* │ │ ├── OpenAIAssistant.py
* │ │ └── requirements.txt
* │ ├── frontend
* │ │ ├── node_modules
* │ │ ├── public
* │ │ └── src
* │ │ │ ├── assets
* │ │ │ └── components
* │ │ │ │ ├── AssistantSelector.vue
* │ │ │ │ ├── ChatDisplay.vue
* │ │ │ │ ├── ChatInput.vue
* │ │ │ │ ├── ChatMessage.vue
* │ │ │ │ ├── HeaderComponent.vue
* │ │ │ │ └── ImageView.vue
* │ │ │ ├── App.vue
* │ │ │ ├── main.ts
* │ │ │ └── shims-vue.d.ts
* │ ├── .browserslistrc
* │ ├── .eslintrc.js
* │ ├── .gitignore
* │ ├── babel.config.js
* │ ├── package.json
* │ ├── package-lock.json
* │ └── tsconfig.json
* 

## Installation

Clone the repository:

1. Navigate to the frontend directory
2. Install dependencies:(`npm install`)
4. Serve the application: (`npm run serve`)

Usage
Frontend

The frontend is built using Vue.js. Messages are managed in a chat format, displaying both user and assistant messages dynamically.
Use the chat interface to send messages, and see responses rendered in real-time.

Components

## Frontend
* App.vue: Main application component that integrates all other components.
* ChatDisplay.vue: Renders the chat messages including user interactions.
* ChatInput.vue: Provides input for new messages to be sent.
* HeaderComponent.vue: Displays the application title and user controls for thread management and assistant handling.


### Handling Messages

The application primarily manages messages using a combination of JavaScript objects, with Vue components observing changes and re-rendering the UI accordingly.
### Message Component

The message component dynamically renders user messages and system messages, applying different styles based on message roles.
### Event Handling

The application fetches data and updates the UI using EventSource to handle server-sent events, allowing for real-time updates without needing to refresh the page.

## Backend
* backend.py


### Setup
Install the required Python packages:
`pip install -r requirements.txt`

Setup the OpenAI API token:
Create a file named openai.json in the backend config directory and add your OpenAI API token:
```json
{
  "organization": "<Your Organization id>",
  "api_key": "<Your OpenAI API Token>",
  "project": "<Project key>",
  "version": "v2.0.0" 
}
```

This file acts as the backend server for the assistant application using Flask. It handles all HTTP requests and serves as the main interface between the frontend and the assistant functionalities.
* Key Features:

    Sets up API endpoints for various functionalities like sending and receiving messages, status streaming, and managing the assistant.
    Implements server-sent events to allow real-time communication with the frontend.
    Initializes the Assistant class which contains the core logic for handling messages, managing threads, and interfacing with the OpenAI API.

Key Endpoints:

    /api/data: A test endpoint returning a simple message from the backend.
    /api/messages: Streams messages to the frontend as they are received or updated.
    /api/status: Streams status messages related to the assistant.
    /api/message: Accepts a POST request to add a new message to the assistant’s context.
    /api/thread/id: Streams the current thread ID to the frontend.
    /api/thread/new: Creates a new thread and returns the thread ID.
    /api/force_update: Forces an update to the assistant’s state.
    /api/assistant: GET to retrieve the current assistant selection and options; POST to set a new assistant.


### Backend Tools

- **Google Search Tool**: Searches for a specified string using the Google Search API.
- **Add Item To YouTube Playlist**: Allows adding a specified video to a designated YouTube playlist.
- **Create Google Calendar Event**: Facilitates the creation of new events in Google Calendar.
- **Create Google Credentials**: Manages the generation and storage of Google API credentials necessary for authentication.
- **Create Google Task**: Enables the creation of new tasks within Google Tasks.
- **Create YouTube Playlist**: Provides the functionality to create a new playlist on YouTube.
- **Get and Parse Email**: Retrieves and processes a spesific email based on ID.
- **Get Current Time and Date**: Retrieves the current time and date in a specified timezone.
- **List Google Calendar Events**: Lists all events scheduled in Google Calendar.
- **List Google Emails**: Provides a list of emails from the user's Gmail account.
- **List Google Tasks**: Retrieves a list of tasks from Google Tasks.
- **List YouTube Playlists**: Fetches and displays all playlists from a specified YouTube channel.
- **Parse Website**: Extracts data from a specified URL using web scraping techniques.
- **Save Important Info**: Saves important user-specific information for later retrieval and reference.
- **Search YouTube Video**: Searches for videos on YouTube based on a given query.

### Example Tool: Text Summarization
This is a hypothetical example tool that summarizes a given text input.

### Structure of the Tool

The tool is structured with a description that outlines its functionality, and a function that performs the summarization:

1. **Tool Description**: This section provides metadata about the tool, including its name, description, and parameters.
    - **Name**: The name of the function (`text_summarization`). (needs to match the function name)
    - **Description**: A brief explanation of what the function does (summarizes a given text).
    - **Parameters**: Specifies the expected input for the function:
        - **Type**: Indicates it is an object.
        - **Properties**: Describes the required parameters:
            - **text**: The actual string that needs summarization, specified as a required field.

2. **Function Implementation**: The actual code that defines how the summarization is performed.
    - **Function `summarizetext)`**: Takes a string input, sends a POST request to an external summarization service, and returns the summary in JSON format.
    - Needs to match the descriptions function name and properties

3. **Main Execution Block**: An example usage of the `summarize` function, which demonstrates how to call it and output the summarized text. Also usefull for testing the tool by itself instead of having to use tokens to test it all the time.
```python
import requests

summarize_description = {
    "type": "function",
    "function": {
        "name": "text_summarization",
        "description": "Summarize a given text.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text that needs to be summarized."
                },
            },
            "required": ["text"]
        },
    }
}

def summarize(text):
    url = 'https://api.summarizationtool.com/summarize'
    response = requests.post(url, json={'text': text})
    return response.json()

if __name__ == "__main__":
    example_text = "This is a long text that needs to be summarized. It talks about various important topics that should be condensed for quicker reading." 
    summary = summarize(example_text)
    print(summary)