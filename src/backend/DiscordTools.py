from datetime import datetime
import tiktoken
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import time
import os
import sqlite3
import json
from openai import OpenAI

from components.utils.utils import set_config_path

set_config_path()


app = Flask(__name__)
CORS(app, origins=["*"])


def num_tokens_from_messages(message, model="gpt-4o-mini"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(message))


# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('C:/dev/discordDataVisualisazion/identifier.sqlite')  # Update to your database path
    conn.row_factory = sqlite3.Row
    return conn


_user_cache = {}


def get_usernames(user_id):
    print(_user_cache)
    conn = get_db_connection()
    # Check if user_id is already cached
    if user_id in _user_cache:
        return _user_cache[user_id]

    # Fetch the username and global name from the database
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, global_name FROM users WHERE id = ?
    """, (user_id,))
    print("making API call for user_id: " + str(user_id))
    result = cursor.fetchone()

    if result:
        # If the user exists, save to cache
        _user_cache[user_id] = {
            'username': result['username'],
            'global_name': result['global_name']
        }
        return result
    else:
        result = {
            "username": "User not found",
            'global_name': "User not found"
        }

        _user_cache[user_id] = {
            'username': result['username'],
            'global_name': result['global_name']
        }
        return result

def messages_to_AI_str(messages):
    return '\n'.join([f'[{m["author"]}] {m["timestamp"]}: {m["content"]}, {m["attachments"]}' for m in messages])

def getDataUntillTokenLimit(token_limit, channel_id='1205881500277547018'):
    conn = get_db_connection()
    def getData(before=None):
        messages = []
        if before is None:
            cursor = conn.execute('SELECT * FROM main.messages WHERE channel_id =? ORDER BY timestamp DESC LIMIT ?',
                                  (channel_id, 10))
        else:
            cursor = conn.execute(
                'SELECT * FROM main.messages WHERE channel_id =? AND timestamp <? ORDER BY timestamp DESC LIMIT ?',
                (channel_id, before, 10))
        rows = cursor.fetchall()
        mints = time.time() * 1000  # Convert to milliseconds
        for row in rows:
            attachments = json.loads(row['attachments'])
            userId = row['user_id']
            print(userId)

            author = get_usernames(userId)['global_name']
            content = row['content']
            ts = row['timestamp']
            if ts < mints:
                mints = ts
            timestamp = datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
            attStr = ''
            if len(attachments) > 0:
                attStr = row['attachments']
            item = {
                'author': author,
                'content': content,
                'timestamp': timestamp,
                'attachments': attStr,
            }

            messages.append(item)
        return messages, mints
    usedTokens = 0
    messages = []
    lastTimestamp = None
    while usedTokens < token_limit:
        lmessages, ts = getData(lastTimestamp)
        lastTimestamp = ts
        messages.extend(lmessages)
        messages.sort(key=lambda x: x['timestamp'], reverse=False)
        ai_input = messages_to_AI_str(messages)
        tokens = num_tokens_from_messages(ai_input)
        usedTokens += tokens
    return messages




if __name__ == '__main__':
    app.run(debug=True, port=5005)
