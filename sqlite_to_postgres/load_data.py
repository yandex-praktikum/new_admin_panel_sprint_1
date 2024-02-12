import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

from sqlite_to_postgres.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from sqlite_to_postgres.sqlite import SQLite
from sqlite_to_postgres.static_data import dsl, sqlite_path


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
            print(table_name)
            SQLite(sqlite_conn).extract_data_and_save_to_postgres(
                model=model,
                table_name=table_name,
                batch_size=20,
                pg_conn=pg_conn,
            )

    sqlite_conn.close()
    pg_conn.close()
