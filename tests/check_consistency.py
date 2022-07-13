import os

import dotenv
import psycopg2
import pytest
from psycopg2.extras import DictCursor

from sqlite_to_postgres.models import (
    Filmwork,
    Genre,
    GenreFilmwork,
    PersonFilmwork,
    Person
)
from utils import Iterator, iter_table_chunked
from utils import (
    sqlite_conn_context,
    load_db_envs,
    PipelineElement,
    convert_timestamp
)


table_names = [
    'film_work',
    'genre',
    'genre_film_work',
    'person',
    'person_film_work',
]

models_mapping = {
    'film_work': Filmwork,
    'genre': Genre,
    'genre_film_work': GenreFilmwork,
    'person': Person,
    'person_film_work': PersonFilmwork,
}

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


@pytest.mark.parametrize(
    'table_name',
    table_names,
)
def test_same_number_of_data_in_tables(table_name: str):
    """Тест проверяет, что количество строк в таблице
    одинаково в обеих базах данных.

    :param table_name: имя таблицы для тестирования
    :type table_name: str
    """
    dotenv.load_dotenv()
    dsl = load_db_envs()
    sqlite_path = os.getenv('SQLITE_PATH')
    pg_schema = 'content'
    with sqlite_conn_context(sqlite_path) as sqlite_conn, psycopg2.connect(
            **dsl,
            cursor_factory=DictCursor
    ) as pg_conn:
        query = f"SELECT COUNT(*) FROM {table_name};"
        curs = sqlite_conn.cursor()
        curs.execute(query)
        sqlite_number = curs.fetchall()[0][0]

        pg_query = f"SELECT COUNT(*) FROM {pg_schema}.{table_name};"
        pg_curs = pg_conn.cursor()
        pg_curs.execute(pg_query)
        pg_number = pg_curs.fetchall()[0][0]

        assert sqlite_number == pg_number


@pytest.mark.parametrize(
    'table_name',
    table_names,
)
def test_same_data_in_tables(table_name: str):
    """Тест проверяет, что данные в таблице одинаковые в обеих базах данных.

    :param table_name: имя таблицы для тестирования
    :type table_name: str
    """
    dotenv.load_dotenv()
    dsl = load_db_envs()
    sqlite_path = os.getenv('SQLITE_PATH')
    pg_schema = 'content'

    with sqlite_conn_context(sqlite_path) as sqlite_conn, psycopg2.connect(
            **dsl,
            cursor_factory=DictCursor
    ) as pg_conn:
        query = f"SELECT * FROM {table_name} ORDER BY id;"
        iterator = Iterator(connection=sqlite_conn)

        pg_query = f"SELECT * FROM {pg_schema}.{table_name} ORDER BY id;"
        pg_iterator = Iterator(connection=pg_conn)

        for p in filter(lambda x: x.table == table_name, pipeline):
            # create data generator with chunks
            iterable_table = iter_table_chunked(
                p=p,
                iterator=iterator,
                chunk_size=50,
                query=query
            )
            pg_iterable_table = iter_table_chunked(
                p=p,
                iterator=pg_iterator,
                chunk_size=50,
                query=pg_query
            )

            for sqlite_data, pg_data in zip(iterable_table, pg_iterable_table):
                if len(sqlite_data) != len(pg_data):
                    raise IndexError
                for i in range(len(sqlite_data)):
                    temp_sqlite = sqlite_data[i]
                    temp_pg = pg_data[i]

                    if hasattr(temp_sqlite, 'created'):
                        temp_sqlite.created = \
                            convert_timestamp(temp_sqlite.created)
                    if hasattr(temp_sqlite, 'modified'):
                        temp_sqlite.modified = \
                            convert_timestamp(temp_sqlite.modified)

                    assert temp_sqlite == temp_pg
