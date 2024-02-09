import sqlite3

import psycopg2
import pytest
from psycopg2.extras import DictCursor
import datetime
from sqlite_to_postgres.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from sqlite_to_postgres.postgres import Postgres
from sqlite_to_postgres.sqlite import SQLite
from sqlite_to_postgres.static_data import sqlite_path, dsl


class TestPostgresAndSqliteConsistency:
    @pytest.mark.parametrize('model, table_name', [
        (FilmWork, 'film_work'),
        (Genre, 'genre'),
        (GenreFilmWork, 'genre_film_work'),
        (Person, 'person'),
        (PersonFilmWork, 'person_film_work')
    ])
    def test_check_table_data(self, model, table_name):
        with sqlite3.connect(sqlite_path, detect_types=sqlite3.PARSE_DECLTYPES) as sqlite_conn, psycopg2.connect(
                **dsl, cursor_factory=DictCursor
        ) as pg_conn:
            sqlite_data = SQLite(connection=sqlite_conn).extract_data(table_name=table_name, model=model)
            postgres_data = Postgres(pg_conn=pg_conn).get_all_data(table_name=table_name, model=model)

            assert len(sqlite_data) == len(postgres_data), 'Количество записей в sqlite и postgres отличается'

            for num, row in enumerate(sqlite_data):
                assert postgres_data[num] == row, 'Строка из postgres отличается от строки из sqlite'
