import os
import sqlite3

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from works import Postgres, SQLite, conn_context, renames_tables, test_data

load_dotenv()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    result: list = []
    """Метод сравнения данных в SQLite и в Postgres"""
    tables = ['genre', 'film_work', 'person', 'genre_film_work',
              'person_film_work']

    for table in tables:
        print("-" * 34)
        print(f"TABLT:\t\t{table}")
        postgres = Postgres(pg_conn)
        sqlite = SQLite(connection)
        data_postgres = postgres.get_data(renames_tables.get(table))
        data_sqlite = sqlite.get_data(table)
        result.append(test_data(data_sqlite, data_postgres))

    print("#" * 34)
    if all(result):
        print('FINALY:\tdata is consistent\tOK')
    else:
        print('FINALY:\tdata is not consistent\ttFAILED')


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
