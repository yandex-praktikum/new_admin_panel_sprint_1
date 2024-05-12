from psycopg2.extensions import connection as _connection
from psycopg2 import IntegrityError
from dataclasses import asdict, astuple


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


class PostgresSaver():
    def __init__(self, pg_conn: _connection) -> None:
        self.conn = pg_conn
        self.scheme = "content"
        self.pg_conn = pg_conn.cursor()

    def save_data(self, data: dict):
        for part in data:
            column_names = [renames_keys.get(part.get('table')).get(key)
                            for key in list(
                                asdict(part.get('data')[0]).keys())]
            column_names_str = ','.join(column_names)
            col_count = ', '.join(['%s'] * len(column_names))
            bind_values = ','.join(self.pg_conn.mogrify(
                f"({col_count})", astuple(user)).decode('utf-8')
                for user in part.get('data'))
            query = (
                f"INSERT INTO {self.scheme}.{renames_tables.get(part.get('table'))} ({column_names_str}) VALUES {bind_values} "
                f" ON CONFLICT (id) DO NOTHING;"
            )

            try:
                self.conn.autocommit = False
                self.pg_conn.execute(query)
                self.conn.commit()
            except IntegrityError as e:
                self.conn.rollback()
                print("*" * 150)
                print(f"MYError: {e}")
            finally:
                self.conn.autocommit = True
