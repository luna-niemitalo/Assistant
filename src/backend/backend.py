# app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import time
import os
import json
from FrontEndMessage import FrontEndMessage
from Assistant import Assistant
from src.backend.DiscordTools import getDataUntillTokenLimit, get_db_connection, messages_to_AI_str
from src.backend.components.utils.utils import set_config_path

set_config_path()


SCOPES = json.load(open(os.path.join(os.environ["CONFIG_PATH"], "scopes.json")))

assistant_options = ["OpenAI_4o", "OpenAI_4o_mini", "LLAMA3"]

app = Flask(__name__)
CORS(app)

assistant = Assistant(assistant_options[1])


@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        json_message = request.get_json(force=True)
        fem = FrontEndMessage(
            text=json_message['text'],
            images=json_message['images'],
            role=json_message['role'],
        )
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

@app.route('/api/discord/data', methods=['GET'])
def discord_ai():
    channelId = request.args.get('channelId')
    print(channelId)
    results = getDataUntillTokenLimit(10000000, channelId)
    print(len(results))
    api_key = json.loads(open(os.path.join(os.getenv('CONFIG_PATH'), 'OpenAI_token.json')).read())['api_key']
    print(api_key)
    return
    client = OpenAI(
        api_key=api_key,
    )
    prompt = messages_to_AI_str(results)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": """
             You are a note taker, provide a brief few sentence summary of the conversation as there will be a lot of data
             Update previous summary, or add extra notes if available.
             Make a short section in the notes for each participants personality and mental state.
             """},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.to_json()

@app.route('/api/discord/messages', methods=['POST', 'GET', 'OPTIONS'])
def post_message():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'content-type': 'application/json',


        }
        return Response(status=200, headers=headers)
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        channel_id = request.args.get('channelId')
        if channel_id is None:
            return jsonify(conn.execute('SELECT * FROM main.messages').fetchall())
        rows = cursor.execute('SELECT id, user_id, channel_id, content, timestamp, attachments FROM messages WHERE channel_id = ?', (channel_id,)).fetchall()
        # Get the column names
        columns = [description[0] for description in cursor.description]
        # Convert rows to a list of dictionaries
        data = [dict(zip(columns, row)) for row in rows]

        return jsonify(data)
    if request.method == 'POST':
        data = request.get_json()
        print("Received message:", data)
        messages = request.json  # Expecting a list of messages in the request
        for message in messages:
            channel_id = message['channelId']
            author_id = message['authorId']
            message_id = message['messageId']
            content = message['content']
            timestamp = message['timestamp']
            attachments = json.dumps(message['attachments'])  # Store attachments as JSON string
            channel_exists = conn.execute('SELECT id FROM main.channels WHERE id = ?', (channel_id,)).fetchone()
            if channel_exists is None:
                conn.execute('INSERT OR IGNORE INTO main.missing_data (type, id) VALUES (?, ?)', ('channel', channel_id))
                conn.commit()

            tsWithSameContent = conn.execute('SELECT timestamp FROM main.messages WHERE content = ?', (content,)).fetchone()
            if tsWithSameContent is not None:
                difference = abs(tsWithSameContent['timestamp'] - timestamp)
                if difference < 10 * 1000:
                    continue
            conn.execute("""INSERT OR IGNORE INTO
            main.messages(id, user_id, channel_id, content, timestamp, attachments)
            VALUES(?, ?, ?, ?, ?, ?)""",
                         (message_id, author_id, channel_id, content, timestamp, attachments))

            conn.commit()
            user_exists = conn.execute('SELECT id FROM main.users WHERE id = ?', (author_id,)).fetchone()
            if user_exists is None:
                conn.execute('INSERT OR IGNORE INTO main.missing_data (type, id) VALUES (?, ?)', ('user', author_id))
                conn.commit()
        conn.close()
        return jsonify({"message": "Message received successfully"}), 201


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


@app.route('/api/assistant', methods=['GET', 'POST'])
def get_assistant():
    if request.method == 'POST':
        selection = request.get_json(force=True)['selection']
        assistant.set_assistant(selection)
        return jsonify({"selection": assistant.selected_assistant, "options": assistant_options})
    if request.method == 'GET':
        return jsonify({"selection": assistant.selected_assistant, "options": assistant_options})


if __name__ == '__main__':
    app.run(debug=True)
