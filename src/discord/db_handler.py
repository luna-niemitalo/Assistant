from flask import jsonify
import mariadb
from pypika import Table, Query, Database, Order, MySQLQuery, Parameter
import json
import os

def create_connection_pool():
    """Creates and returns a Connection Pool"""

    # Create Connection Pool
    pool = mariadb.ConnectionPool(
        user=os.environ['MYSQL_DISCORD_USER'],
        password=os.environ['MYSQL_DISCORD_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        port=3306,
        database=os.environ['MYSQL_DISCORD_DATABASE'],
        pool_name="web-app",
        pool_size=20,
        pool_validation_interval=250)

    # Return Connection Pool
    return pool


def insert_item(data, t):
    """Insert new item into the database."""
    q = MySQLQuery.into(t).columns(*data.keys()).insert(
        *(Parameter('%s') for _ in data.values())
    )

    # Convert lists to JSON strings in the data values
    params = [serialize_value(v) for v in data.values()]

    # Print SQL for debugging
    print(q.get_sql())
    result = (q.get_sql(), params)
    return result

def update_item(data, t, item_id):
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
        result = (q.get_sql(), params)
        return result

def serialize_value(value):
    """Convert lists to JSON strings for storage in MariaDB, leave other types unchanged."""
    return json.dumps(value) if isinstance(value, list) else value

class DiscordDBHandler:
    def __init__(self):
        print("Initializing DiscordDBHandler 2")
        self.conn_pool = create_connection_pool()

    def check_existing_item(self, t, item_id):
        pconn = self.conn_pool.get_connection()
        cursor = pconn.cursor()
        """Check if an item with the specified ID already exists in the database."""
        select_query = MySQLQuery.from_(t).select(t.star).where(t.id == item_id)
        cursor.execute(select_query.get_sql() + 'LIMIT 1 FOR UPDATE')
        result = cursor.fetchone()
        pconn.close()
        return result


    def get_paginated_data(
            self,
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
        pconn = self.conn_pool.get_connection()
        cursor = pconn.cursor()
        cursor.execute(q.get_sql())
        rows = cursor.fetchall()
        pconn.close()

        num_fields = len(cursor.description)
        field_names = [i[0] for i in cursor.description]
        #label results to dictionary
        result = []
        for row in rows:
            result.append(dict(zip(field_names, row)))

        return result

    def get_data_by_id(self, table, id):
        pconn = self.conn_pool.get_connection()
        t = Table(table)
        q = MySQLQuery.from_(t)
        q = q.select("*")
        q= q.where(t.id == id)
        cursor = pconn.cursor()
        cursor.execute(q.get_sql())
        row = cursor.fetchone()
        pconn.close()
        field_names = [i[0] for i in cursor.description]

        if row is not None:
            return dict(zip(field_names, row))
        else:
            return None



    def upsert_data(self, table, data):
        """Upsert function that inserts or updates data depending on whether an item exists."""
        t = Table(table)
        item_id = data.get("id")

        # Step 1: Check if item with matching ID exists in the database
        existing_item = self.check_existing_item(t, item_id)

        # Step 2: Decide between insert and update
        if not existing_item:
            query = insert_item(data, t)
        else:
            query = update_item(data, t, item_id)

        print(data)
        pconn = self.conn_pool.get_connection()
        cursor = pconn.cursor()
        print("cursor built")
        cursor.execute(*query)
        print("cursor executed")
        pconn.commit()



