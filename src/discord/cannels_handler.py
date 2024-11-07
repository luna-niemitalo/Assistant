from flask import jsonify

from src.discord.db_handler import get_data_by_id, get_paginated_data, upsert_data
from src.discord.utils import build_db_channel


def get_handler(conn, params):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = get_data_by_id(conn, "channels", id=id)
        return jsonify(data)
    else:
        # Handle GET request to get guilds
        data = get_paginated_data(conn, "channels")
        return jsonify(data)

def post_handler(conn, data):
    print("Received channel:")
    print(data)
    db_channel = build_db_channel(data)
    # Insert or update channel data in the database
    result = upsert_data(conn, "channels", db_channel)
    print(f"Inserted/updated channel ID: {result}")

    return jsonify({"message": "Channel received successfully"}), 201
