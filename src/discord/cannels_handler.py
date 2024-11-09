from flask import jsonify

from db_handler import DiscordDBHandler
from utils import build_db_channel


def get_handler( params, db_handler: DiscordDBHandler):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = db_handler.get_data_by_id("channels", id=id)
        return jsonify(data)
    else:
        # Handle GET request to get guilds
        data = db_handler.get_paginated_data("channels")
        return jsonify(data)

def post_handler(data, db_handler: DiscordDBHandler):
    print("Received channel:")
    print(data)
    db_channel = build_db_channel(data)
    # Insert or update channel data in the database
    db_handler.upsert_data("channels", db_channel)

    return jsonify({"message": "Channel received successfully"}), 201
