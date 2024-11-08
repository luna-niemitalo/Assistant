from flask import jsonify

from src.discord.db_handler import DiscordDBHandler

def get_handler(params, db_handler: DiscordDBHandler):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = db_handler.get_data_by_id("users", id=id)
        return jsonify(data)
    else:
        limit = params.get("limit", default=30, type=int)
        after = params.get("after", type=int)
        has_mutuals = params.get("has_mutuals", type=int)

        # Handle GET request to get users
        data = db_handler.get_paginated_data("users", page_size=limit, after=after, has_mutuals=has_mutuals)
        return jsonify(data)