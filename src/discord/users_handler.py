from flask import jsonify

from src.discord.db_handler import get_data_by_id, get_paginated_data

def get_handler(conn, params):
    id = params.get("id", type=int)
    if id:
        # Handle GET request to get guild by ID
        data = get_data_by_id(conn, "users", id=id)
        return jsonify(data)
    else:
        limit = params.get("limit", default=30, type=int)
        after = params.get("after", type=int)
        has_mutuals = params.get("has_mutuals", type=int)

        # Handle GET request to get users
        data = get_paginated_data(conn, "users", page_size=limit, after=after, has_mutuals=has_mutuals)
        return jsonify(data)