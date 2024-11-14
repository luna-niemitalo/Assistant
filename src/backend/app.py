# app.py
import flask
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import time
import os
import json
from FrontEndMessage import FrontEndMessage
from Assistant import Assistant
from DiscordTools import getDataUntillTokenLimit, get_db_connection, messages_to_AI_str
from components.utils.utils import set_config_path, build_db_message

set_config_path()

SCOPES = json.load(open(os.path.join(os.environ["CONFIG_PATH"], "scopes.json")))

assistant_options = ["OpenAI_4o_full", "OpenAI_4o_mini", "LLAMA3"]

app = Flask(__name__)
CORS(app)

assistant = Assistant(assistant_options[1])


@app.route('/', methods=['GET'])
def default():
    # Test webserver
    return jsonify("Hello, World!")


@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        json_message = request.get_json(force=True)

        db_message = build_db_message(json_message)
        print("Received message: ", db_message)
        timestamp = db_message['timestamp']
        # TODO: Convert TS to datetime
        content = db_message['content']
        user_id = db_message['user_id']
        # TODO: Fetch username from Database

        embeds = db_message['embeds']
        components = db_message['components']
        attachments = db_message['attachments']
        mentions = db_message['mentions']
        #reference = db_message.reference
        # TODO: Fetch referred message from Database

        text = f"[{timestamp}: {user_id}] {content} \n "
        if embeds:
            text += f"{embeds}\n"
        if components:
            text += f"\nComponents: {components}\n"
        if attachments:
            text += f"\nAttachments: {attachments}\n"
        if mentions:
            text += f"\nMentions: {mentions}\n"
        print(text)
        fem = FrontEndMessage(text=text, images=[], role="user")
        result = assistant.add_message(fem)
        print("Result: ", result.get_fem())
        return json.dumps(result.get_fem())
    if request.method == 'GET':
        def event_stream():
            prev_length = 0
            force_update = assistant.get_force_update()
            while True:
                fem = assistant.get_messages()
                if len(fem) != prev_length or force_update["messages"]:
                    yield f"data: {json.dumps([message.get_fem() for message in fem])}\n\n"
                    force_update["messages"] = False
                    prev_length = len(fem)
                time.sleep(0.1)

        return Response(event_stream(), mimetype="text/event-stream")


@app.route('/api/status', methods=['GET'])
def status_stream():
    def event_stream():
        old_len = 0
        force_update = assistant.get_force_update()
        while True:
            if len(assistant.status_messages) > old_len or force_update["status"]:
                old_len = len(assistant.status_messages)
                force_update["status"] = False
                yield f"data: {json.dumps(assistant.status_messages)}\n\n"
            else:
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


@app.route('/api/open_ai_image', methods=['GET'])
def open_ai_image():
    image_id = request.args.get('image_id')
    return assistant.get_openai_image(image_id)


@app.route('/api/thread', methods=['GET', 'POST'])
def messages_thread():
    if request.method == 'POST':
        result = assistant.new_thread()
        assistant.set_force_update()
        return result
    if request.method == 'GET':
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


@app.route('/api/force_update', methods=['GET'])
def force_update():
    assistant.set_force_update()
    return jsonify({"status": "success"})


@app.route('/api/bottest', methods=['POST', 'OPTIONS'])
def bot_test():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'content-type': 'application/json',
        }
        return Response(status=200, headers=headers)

    if request.method == 'POST':
        data = request.get_json()
        print("Received message:", data)
        return jsonify({"message": "Message received successfully"}), 202

    return jsonify({"message": "Invalid request method"}), 405


@app.route('/api/assistant', methods=['GET', 'POST'])
def get_assistant():
    if request.method == 'POST':
        selection = request.get_json(force=True)['selection']
        assistant.set_assistant(selection)
        return jsonify({"selection": assistant.selected_assistant, "options": assistant_options})
    if request.method == 'GET':
        return jsonify({"selection": assistant.selected_assistant, "options": assistant_options})


if __name__ == '__main__':
    app.run(debug=True, port=5010, host='0.0.0.0')
