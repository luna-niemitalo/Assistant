# app.py
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from db_handler import DiscordDBHandler

app = Flask(__name__)
CORS(app)


db_handler = DiscordDBHandler()

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
        from  users_handler import get_handler
        return get_handler(request.args, db_handler)
    if request.method == "POST":
        from users_handler import post_handler
        data = request.get_json()
        return post_handler(data, db_handler)
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
        from guilds_handler import get_handler
        return get_handler(request.args, db_handler)
    if request.method == "POST":
        from guilds_handler import post_handler
        data = request.get_json()
        return post_handler(data, db_handler)
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
        from cannels_handler import get_handler
        return get_handler(request.args, db_handler)
    if request.method == "POST":
        from cannels_handler import post_handler
        data = request.get_json()
        return post_handler(data, db_handler)
    return jsonify({"message": "Not implemented"}), 501


@app.route("/api/messages", methods=["GET", "POST", "OPTIONS"])
def messages():
    # Handle GET request to get messages
    if request.method == "GET":
        from messages_handler import get_handler
        return get_handler(request.args, db_handler)

    if request.method == 'POST':
        data = request.get_json()
        print("Received message:", data)
        from messages_handler import post_handler
        return post_handler(data, db_handler)
    return jsonify({"message": "Not implemented"}), 501



if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, port=5020, host='0.0.0.0')
