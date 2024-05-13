import os
import sqlite3

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from read_data import SQLiteExtractor, conn_context
from write_data import PostgresSaver

load_dotenv()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver.save_data(sqlite_extractor.extract_movies())


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME', 'movies_database'),
        'user': os.environ.get('DB_USER', 'app'),
        'password': os.environ.get('DB_PASSWORD', '123qwe'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', '5432'))
    }

    try:
        with conn_context('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
    except Exception as e:
        print(f"ERROR: {str(e)}")
