from flask import jsonify
import json

from db_handler import DiscordDBHandler
from utils import build_db_message, build_db_user


def get_handler(params, db_handler: DiscordDBHandler):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = db_handler.get_data_by_id( "messages", id=id)
        return jsonify(data)
    else:
        limit = params.get("limit", default=30, type=int)
        user_id = params.get("user_id", type=int)
        channel_id = params.get("channel_id", type=int)
        after = params.get("after", type=int)
        # Handle GET request to get guilds
        data = db_handler.get_paginated_data("messages", page_size=limit, after=after, limit_user_id=user_id, limit_channel_id=channel_id)
        return jsonify(data)

def post_handler( data, db_handler: DiscordDBHandler):
    print("Received message:")
    db_obj = build_db_message(data['data'])
    db_user = build_db_user(data['author'])
    db_handler.upsert_data( "messages", db_obj)
    db_handler.upsert_data("users", db_user)

    return jsonify({"message": "Message received successfully"}), 201
