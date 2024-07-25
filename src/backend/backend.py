# app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import time
import os
import json
from FrontEndMessage import FrontEndMessage
from Assistant import Assistant

print(os.getcwd())
path = os.path.join(os.getcwd(), "config")
print(path)
os.environ["CONFIG_PATH"] = path

SCOPES = json.load(open(os.path.join(os.environ["CONFIG_PATH"], "scopes.json")))

assistant_options = ["OpenAI_4o", "OpenAI_4o_mini", "LLAMA3"]

app = Flask(__name__)
CORS(app)

assistant = Assistant(assistant_options[1])


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
            force_update = assistant.get_force_update()
            if len(fem) != prev_length or force_update:
                yield f"data: {json.dumps([message.get_fem() for message in fem])}\n\n"
                assistant.force_update = False
                prev_length = len(fem)
            time.sleep(0.1)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route('/api/status', methods=['GET'])
def status_stream():
    def event_stream():
        old_len = 0
        while True:
            if len(assistant.status_messages) > old_len:
                old_len = len(assistant.status_messages)
                yield f"data: {json.dumps(assistant.status_messages)}\n\n"
            else:
                time.sleep(0.3)

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
    json_message = request.get_json(force=True)
    fem = FrontEndMessage(
        text=json_message['text'],
        images=json_message['images'],
        role=json_message['role'],
    )
    result = assistant.add_message(fem)
    print("Result: ", result.get_fem())
    return json.dumps(result.get_fem())


@app.route('/api/open_ai_image', methods=['GET'])
def open_ai_image():
    image_id = request.args.get('image_id')
    return assistant.get_openai_image(image_id)


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


@app.route('/api/assistant', methods=['GET'])
def get_assistant():
    return jsonify({"selection": assistant.selected_assistant, "options": assistant_options})

@app.route('/api/assistant', methods=['POST'])
def set_assistant():
    selection = request.get_json(force=True)['selection']
    assistant.set_assistant(selection)
    return jsonify({"selection": assistant.selected_assistant, "options": assistant_options})


if __name__ == '__main__':
    app.run(debug=True)
