from flask import jsonify
from pypika import Table, Query, Database, Order, MySQLQuery, Parameter
import json

def get_paginated_data(
        conn,
        table,
        columns = "*",
        page_size = None,
        after=None,
        limit_user_id=None,
        limit_channel_id=None,
        has_mutuals=None,
):
    t = Table(table)
    q = MySQLQuery.from_(t)
    if columns is not None:
        for column in columns:
            q = q.select(column)
    q = q.limit(page_size)
    q = q.orderby(t.id, order=Order.desc)

    if after is not None:
        q = q.where(t.id < after)

    if has_mutuals is not None:
        q = q.where(t.mutual_friends_count >= has_mutuals)

    if limit_user_id is not None:
        q = q.where(t.user_id == limit_user_id)
    if limit_channel_id is not None:
        q = q.where(t.channel_id == limit_channel_id)
    print(q.get_sql())
    cursor = conn.cursor()
    cursor.execute(q.get_sql())
    rows = cursor.fetchall()

    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
    #label results to dictionary
    result = []
    for row in rows:
        result.append(dict(zip(field_names, row)))

    return result

def get_data_by_id(conn, table, id):
    t = Table(table)
    q = MySQLQuery.from_(t)
    q = q.select("*")
    q= q.where(t.id == id)
    cursor = conn.cursor()
    cursor.execute(q.get_sql())
    row = cursor.fetchone()
    field_names = [i[0] for i in cursor.description]

    if row is not None:
        return dict(zip(field_names, row))
    else:
        return None

def serialize_value(value):
    """Convert lists to JSON strings for storage in MariaDB, leave other types unchanged."""
    return json.dumps(value) if isinstance(value, list) else value

def upsert_data(conn, table, data):
    """Upsert function that inserts or updates data depending on whether an item exists."""
    t = Table(table)
    item_id = data.get("id")
    cursor = conn.cursor()

    # Step 1: Check if item with matching ID exists in the database
    existing_item = check_existing_item(conn, t, item_id)

    # Step 2: Decide between insert and update
    if not existing_item:
        insert_item(cursor, data, t)
    else:
        update_item(cursor, data, t, item_id)

    print(data)
    # Commit transaction and return lastrowid for inserts
    conn.commit()

def check_existing_item(conn, t, item_id):
    cursor = conn.cursor()
    """Check if an item with the specified ID already exists in the database."""
    select_query = MySQLQuery.from_(t).select(t.star).where(t.id == item_id)
    cursor.execute(select_query.get_sql() + 'LIMIT 1 FOR UPDATE')
    result = cursor.fetchone()
    return result

def insert_item(cursor, data, t):
    """Insert new item into the database."""
    q = MySQLQuery.into(t).columns(*data.keys()).insert(
        *(Parameter('%s') for _ in data.values())
    )

    # Convert lists to JSON strings in the data values
    params = [serialize_value(v) for v in data.values()]

    # Print SQL for debugging
    print(q.get_sql())
    cursor.execute(q.get_sql(), params)

def update_item(cursor, data, t, item_id):
    """Update existing item in the database with new values where they are provided."""
    # Only update fields that are non-None and non-empty
    update_fields = {
        k: Parameter('%s') for k, v in data.items()
        if v is not None and (not isinstance(v, list) or len(v) > 0) and k != "id"
    }

    if update_fields:
        q = MySQLQuery.update(t).where(t.id == item_id)

        # Add each field individually using a loop
        for field, value in update_fields.items():
            q = q.set(getattr(t, field), Parameter('%s'))

        # Convert lists to JSON strings in the update parameters
        params = [serialize_value(data[k]) for k in update_fields.keys()]

        # Print SQL for debugging
        print(q.get_sql())
        cursor.execute(q.get_sql(), params)