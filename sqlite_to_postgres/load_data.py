import sqlite3
from dataclasses import dataclass

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_to_postgres.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from sqlite_to_postgres.postgres import Postgres
from sqlite_to_postgres.sqlite import SQLite
from sqlite_to_postgres.static_data import dsl, sqlite_path


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, table_name: str, model: dataclass):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = Postgres(pg_conn)
    sqlite_extractor = SQLite(connection)

    data = sqlite_extractor.extract_data(model=model, table_name=table_name)
    postgres_saver.save_all_data(table_name=table_name, insert_data=data)


if __name__ == "__main__":

    data_to_extract = [
        (FilmWork, 'film_work'),
        (Genre, 'genre'),
        (GenreFilmWork, 'genre_film_work'),
        (Person, 'person'),
        (PersonFilmWork, 'person_film_work')
    ]
    with sqlite3.connect(sqlite_path) as sqlite_conn, psycopg2.connect(
        **dsl, cursor_factory=DictCursor
    ) as pg_conn:
        for model, table_name in data_to_extract:
            load_from_sqlite(sqlite_conn, pg_conn, model=model, table_name=table_name)
