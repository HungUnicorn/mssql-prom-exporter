import logging

import pymssql
from flask import current_app as app

LOGGER = logging.getLogger(__name__)


def get_connection():
    server = app.config["SERVER"]
    user = app.config["USERNAME"]
    password = app.config["PASSWORD"]
    conn = pymssql.connect(server, user, password)
    return conn


def get_query_result(conn, query):
    with conn.cursor(as_dict=True) as cursor:
        try:
            cursor.execute(query)
            for row in cursor:
                yield row
        except pymssql.DatabaseError as e:
            LOGGER.error("Query: %s has error: %s", query, str(e))
