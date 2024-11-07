from flask import jsonify

from src.discord.db_handler import get_data_by_id, get_paginated_data


def get_handler(conn, params):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = get_data_by_id(conn, "guilds", id=id)
        return jsonify(data)
    else:
        # Handle GET request to get guilds
        data = get_paginated_data(conn, "guilds")
        return jsonify(data)
