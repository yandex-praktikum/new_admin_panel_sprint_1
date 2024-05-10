import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from read_data import SQLiteExtractor
from write_data import PostgresSaver
from contextlib import contextmanager


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    for _ in data:    
        print(_.get('table'))
        print(_.get('data'))

    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe',
           'host': '127.0.0.1', 'port': 5432}
    with conn_context('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
