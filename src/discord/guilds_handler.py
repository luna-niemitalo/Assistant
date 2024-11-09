from flask import jsonify

from db_handler import DiscordDBHandler
from utils import build_db_guild


def get_handler(params,  db_handler: DiscordDBHandler):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = db_handler.get_data_by_id( "guilds", id=id)
        return jsonify(data)
    else:
        # Handle GET request to get guilds
        data = db_handler.get_paginated_data( "guilds")
        return jsonify(data)

def post_handler(data, db_handler: DiscordDBHandler):
    print("Received guild:")
    print(data)
    # Insert or update guild data in the database
    db_guild = build_db_guild(data)
    db_handler.upsert_data("guilds", db_guild)
    return jsonify({"message": "Guild received successfully"}), 201

