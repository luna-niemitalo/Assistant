from flask import jsonify
import json

from src.discord.db_handler import get_data_by_id, get_paginated_data, upsert_data
from src.discord.utils import build_db_message, build_db_user


def get_handler(conn, params):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = get_data_by_id(conn, "messages", id=id)
        return jsonify(data)
    else:
        limit = params.get("limit", default=30, type=int)
        user_id = params.get("user_id", type=int)
        channel_id = params.get("channel_id", type=int)
        after = params.get("after", type=int)
        # Handle GET request to get guilds
        data = get_paginated_data(conn, "messages", page_size=limit, after=after, limit_user_id=user_id, limit_channel_id=channel_id)
        return jsonify(data)

def post_handler(conn, data):
    print("Received message:")
    db_obj = build_db_message(data['data'])
    db_user = build_db_user(data['author'])
    upsert_data(conn, "messages", db_obj)
    #upsert_data(conn, "users", db_user)

    return jsonify({"message": "Message received successfully"}), 201
