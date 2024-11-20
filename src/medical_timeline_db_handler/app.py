import time
from datetime import datetime

from flask import jsonify
import mariadb
from pypika import Table, Query, Database, Order, MySQLQuery, Parameter
import json
import os
from flask import Flask, jsonify, request, Response, render_template
from flask_cors import CORS
from sqlalchemy.testing.plugin.plugin_base import logging

app = Flask(__name__)
CORS(app)

def create_connection_pool():
    """Creates and returns a Connection Pool"""
    # Create Connection Pool
    pool = mariadb.ConnectionPool(
        user=os.environ['MYSQL_MED_USER'],
        password=os.environ['MYSQL_MED_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        port=3306,
        database=os.environ['MYSQL_MED_DATABASE'],
        pool_name="web-app",
        pool_size=20,
        pool_validation_interval=250)

    # Return Connection Pool
    return pool

pool = create_connection_pool()
# Load the tag mapping from the JSON file
with open("tag_mapping.json") as f:
    TAG_MAPPING = {int(k): v for k, v in json.load(f).items()}
    TAG_REVERSE_MAPPING = {v: k for k, v in TAG_MAPPING.items()}

def get_tags_from_binary(binary):
    """
    Converts a binary number to an array of tags based on the mapping.
    """
    tags = []
    for key, tag in TAG_MAPPING.items():
        if binary & key:  # Check if this bit is active
            tags.append(tag)
    return tags

def get_binary_from_tags(tag_list):
    """
    Converts a list of tags to a binary representation based on the mapping.
    """
    binary = 0
    for tag in tag_list:
        if tag in TAG_REVERSE_MAPPING:
            binary |= TAG_REVERSE_MAPPING[tag]
    return binary

# Serve index.html at the root endpoint
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tags/mapping', methods=['GET'])
def get_tag_mapping():
    """
    Endpoint to retrieve the tag mapping JSON data for external clients.
    """
    return jsonify(TAG_MAPPING)

@app.route('/tags/from_binary', methods=['POST'])
def tags_from_binary():
    """
    Converts a binary representation to tags.
    Request JSON should contain a field "binary".
    """
    data = request.get_json()
    binary = data.get("binary")

    if binary is None:
        return jsonify({"error": "Missing 'binary' field"}), 400

    tags = get_tags_from_binary(binary)
    return jsonify({"tags": tags})

@app.route('/tags/to_binary', methods=['POST'])
def binary_from_tags():
    """
    Converts a list of tags to a binary representation.
    Request JSON should contain a field "tags" with an array of tag names.
    """
    data = request.get_json()
    tag_list = data.get("tags")

    if not isinstance(tag_list, list):
        return jsonify({"error": "Invalid or missing 'tags' field"}), 400

    binary = get_binary_from_tags(tag_list)
    return jsonify({"binary": binary})


# POST endpoint for adding an event
@app.route('/events', methods=['POST'])
def create_event():
    conn = pool.get_connection()
    # Parse JSON data from the request
    data = request.get_json()

    # Generate a UUID for the event
    user_id = data.get('user_id')
    title = data.get('title')
    created_at = time.time()
    print(created_at)
    event_type = data.get('event_type')
    timestamp = data.get('timestamp')
    falloff_range = data.get('falloff_range')  # For 'around' events
    start_timestamp = data.get('start_timestamp')  # For 'between' events
    end_timestamp = data.get('end_timestamp')      # For 'between' events
    notes = data.get('notes', '')
    severity = data.get('severity')                # Severity for symptoms
    symptom = data.get('symptom', False)           # Boolean, default to False
    category = data.get('category', '')            # Flexible text category
    tags = data.get('tags', 0)                 # Array of tag IDs

    # Severity validation: Only for symptom events, float between 1.0 and 10.0
    if symptom and (severity is None or not (0.0 <= severity <= 10.0)):
        return jsonify({"error": "Severity must be a float between 1 and 10 for symptom events"}), 400

    conn = pool.get_connection()
    # Validate required fields
    if not (user_id and title and event_type in {'at', 'around', 'between'}):
        return jsonify({"error": "Missing required fields or invalid event type"}), 400

    # Validate timestamp format

    # Database insertion
    try:
        cursor = conn.cursor()

        # Insert into Events table
        cursor.execute("""
            INSERT INTO Events ( user_id, title, created_at, event_type, 
                                timestamp, falloff_range, start_timestamp, end_timestamp, notes, severity, symptom, category, tags)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ( user_id, title, created_at, event_type, timestamp,
              falloff_range, start_timestamp, end_timestamp, notes, severity, symptom, category, tags))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Event created successfully"}), 201

    except conn.DatabaseError as err:
        print(f"Error: {err}")
        return jsonify({"error": "Database error occurred"}), 500


if __name__ == "__main__":

    print("Starting Flask server...")
    app.run(debug=True, port=5040, host='0.0.0.0')