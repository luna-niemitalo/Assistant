from flask import jsonify

from src.discord.db_handler import DiscordDBHandler


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
