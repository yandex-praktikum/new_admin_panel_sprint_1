import os
import sqlite3

import dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from iterator import Iterator, iter_table_chunked
from loader import Loader
from models import (
    Filmwork,
    Genre,
    GenreFilmwork,
    PersonFilmwork,
    Person
)
from utils import PipelineElement, sqlite_conn_context

rename_created_at = {'created_at': 'created'}
rename_updated_at = {'updated_at': 'modified'}

# Пайплайн обработки данных с настройками
pipeline = [
    PipelineElement(
        table='film_work',
        model=Filmwork,
        fields_to_rename={
            **rename_created_at,
            **rename_updated_at
        }
    ),
    PipelineElement(
        table='genre',
        model=Genre,
        fields_to_rename={
            **rename_created_at,
            **rename_updated_at
        },
        skip_empty_fields=['description']
    ),
    PipelineElement(
        table='genre_film_work',
        model=GenreFilmwork,
        fields_to_rename={
            **rename_created_at
        }
    ),
    PipelineElement(
        table='person',
        model=Person,
        fields_to_rename={
            **rename_created_at,
            **rename_updated_at
        }
    ),
    PipelineElement(
        table='person_film_work',
        model=PersonFilmwork,
        fields_to_rename={
            **rename_created_at,
            **rename_updated_at
        }
    )
]


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection,
        chunk_size: int = 50
):
    """Основной метод загрузки данных из SQLite в Postgres"""
    loader = Loader(connection=pg_conn, chunk_size=chunk_size)
    iterator = Iterator(connection=connection)

    for p in pipeline:
        # create data generator with chunks
        iterable_table = iter_table_chunked(
            p=p,
            iterator=iterator,
            chunk_size=chunk_size
        )

        for i in iterable_table:
            # save data in another db with chunks
            loader.load_from_iterable(
                items=i,
                dataclass=p.model,
                table_name=p.table
            )


if __name__ == '__main__':
    dotenv.load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    with sqlite_conn_context('db.sqlite') as sqlite_conn, psycopg2.connect(
            **dsl,
            cursor_factory=DictCursor
    ) as pg_conn:
        chunk_size = 50
        load_from_sqlite(sqlite_conn, pg_conn, chunk_size)
