# discord_endpoint.py
import mariadb
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from waitress.compat import MAXINT

from src.discord.db_handler import get_paginated_data, get_data_by_id

app = Flask(__name__)
CORS(app)

conn = None

@app.route("/", methods=["GET"])
def hello_world():
    return {"message": "Hello, World!"}



@app.route("/api/users", methods=["GET", "POST", "OPTIONS"])
def users():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'content-type': 'application/json',
        }
        return Response(status=200, headers=headers)
    if request.method == "GET":
        from  src.discord.users_handler import get_handler
        return get_handler(conn, request.args)
    return jsonify({"message": "Not implemented"}), 501



@app.route("/api/guilds", methods=["GET", "POST", "OPTIONS"])
def guilds():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'content-type': 'application/json',
        }
        return Response(status=200, headers=headers)
    if request.method == "GET":
        from src.discord.guilds_handler import get_handler
        return get_handler(conn, request.args)
    return jsonify({"message": "Not implemented"}), 501


@app.route("/api/channels", methods=["GET", "POST", "OPTIONS"])
def channels():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'content-type': 'application/json',
        }
        return Response(status=200, headers=headers)
    if request.method == "GET":
        from src.discord.cannels_handler import get_handler
        return get_handler(conn, request.args)
    return jsonify({"message": "Not implemented"}), 501


@app.route("/api/messages", methods=["GET", "POST", "OPTIONS"])
def messages():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'content-type': 'application/json',
        }
        return Response(status=200, headers=headers)
    # Handle GET request to get messages
    if request.method == "GET":
        from src.discord.messages_handler import get_handler
        return get_handler(conn, request.args)

    if request.method == 'POST':
        data = request.get_json()
        from src.discord.messages_handler import post_handler
        return post_handler(conn, data)
    return jsonify({"message": "Not implemented"}), 501


if __name__ == "__main__":
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="discord_bot",
            password="976431258",
            host="ebin.spurdo.us",
            port=3306,
            database="discord"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(1)

    app.run(debug=True, port=5020, host='0.0.0.0')
