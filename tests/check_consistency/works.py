import sqlite3
from psycopg2.extensions import connection as _connection
from psycopg2 import IntegrityError
from contextlib import contextmanager


renames_tables = {
    'genre': 'genre',
    'film_work': 'filmwork',
    'person': 'person',
    'genre_film_work': 'genre_film_work',
    'person_film_work': 'person_film_work'
}

renames_keys = {
    'genre': {
        'name': 'name',
        'created_at': 'created',
        'updated_at': 'modified',
        'description': 'description',
        'id': 'id'
    },
    'film_work': {
        'title': 'title',
        'type': 'type',
        'created_at': 'created',
        'updated_at': 'modified',
        'id': 'id',
        'description': 'description',
        'creation_date': 'premiere_date',
        'file_path': 'file_path',
        'rating': 'rating'
    },
    'person': {
        'full_name': 'full_name',
        'created_at': 'created',
        'updated_at': 'modified',
        'id': 'id'
    },
    'genre_film_work': {
        'created_at': 'created',
        'id': 'id',
        'film_work_id': 'film_work_id',
        'genre_id': 'genre_id'
    },
    'person_film_work': {
        'role': 'role',
        'created_at': 'created',
        'id': 'id',
        'film_work_id': 'film_work_id',
        'person_id': 'person_id'
    }
}


class SQLite():

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.sl_conn = connection

    def get_data(self, table):
        curs = self.sl_conn.cursor()
        curs.execute(f"SELECT * FROM {table};")
        data = curs.fetchall()
        return {"table": table, 'data': [dict(_) for _ in data]}


class Postgres():

    def __init__(self, pg_conn: _connection) -> None:
        self.conn = pg_conn
        self.scheme = "content"
        self.pg_conn = pg_conn.cursor()

    def get_data(self, table):
        try:
            self.conn.autocommit = False
            self.pg_conn.execute(f"SELECT * FROM {self.scheme}.{table};")
            self.conn.commit()
        except IntegrityError as e:
            self.conn.rollback()
            print(f"Error: {e}")
        finally:
            self.conn.autocommit = True
        data = self.pg_conn.fetchall()
        return {"table": table, 'data': [dict(_) for _ in data]}


def test_data(SQLite_tatle: dict, Postgres_table: dict) -> bool:
    result: list = []
    result_data: list = []
    keys1 = renames_keys.get(SQLite_tatle['table'])
    keys2 = renames_keys.get(SQLite_tatle['table']).values()
    SQLite_data = []
    Postgres_data = []

    """ Переименовение ключей для таблиц SQLite """
    for line in list(SQLite_tatle['data']):
        SQLite_data.append(sorted({keys1.get(k): x for k, x in line.items()}))

    """ Исключение ключей которых нету для таблиц Postgres """
    for line in list(Postgres_table['data']):
        Postgres_data.append(sorted({k: x for k, x in line.items() if k in keys2}))

    """ Сравнение колличества записей в БД """
    if len(SQLite_tatle.get('data')) == len(Postgres_table.get('data')):
        result.append(True)
        print(f"TEST LEN:\t{len(SQLite_tatle.get('data'))}"
              f" == {len(Postgres_table.get('data'))}\tOK")
    else:
        print(f"TEST LEN:\t{len(SQLite_tatle.get('data'))} \
              <> {len(Postgres_table.get('data'))}\tFAILED")
        result.append(False)

    """ Сравнение записей в БД """
    for line1 in SQLite_data:
        if line1 in Postgres_data:
            result_data.append(True)
        else:
            print(f"FAILED LINE: {line1}")
            result_data.append(False)

    if all(result_data) is True:
        print("TEST DATA:\t\t\tOK")
        result.append(True)
    else:
        print("TEST DATA:\t\t\tFAILED")
        result.append(False)

    return all(result)


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
