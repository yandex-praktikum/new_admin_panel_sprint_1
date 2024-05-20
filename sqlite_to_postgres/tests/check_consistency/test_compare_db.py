import datetime
import os
import pathlib
import sqlite3
from contextlib import closing, contextmanager
from typing import Generator

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from sqlite_to_postgres.models import MODELS

BATCH_SIZE = 1000


@pytest.fixture(scope="session", autouse=True)
def load_env():
    CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
    PROJECT_BASE_DIR = CURRENT_DIR.parent.parent
    load_dotenv(str(PROJECT_BASE_DIR.parent.joinpath("movies_admin/config/.env")))
    sqlite_db = PROJECT_BASE_DIR.joinpath(os.environ.get("SQLITE_BASE", "db.sqlite"))
    dsl_config = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": os.environ.get("DB_PORT", 5432),
        "options": f'-c search_path={os.environ.get("SCHEMA")}',
    }
    return sqlite_db, dsl_config


@contextmanager
def conn_context(db_path: str) -> Generator:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@pytest.mark.parametrize("model", MODELS)
def test_rows_cnt(load_env, model):
    db_path, dsl = load_env

    with (
        conn_context(db_path) as sqlite_conn,
        closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn,
    ):
        query = f"SELECT count(*) FROM {model._table_name};"
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute(query)
        sqlite_result = sqlite_cur.fetchone()

        pg_cur = pg_conn.cursor()
        pg_cur.execute(query)
        pg_result = pg_cur.fetchone()

        assert sqlite_result[0] == pg_result[0]


@pytest.mark.parametrize("model", MODELS)
def test_rows_equality(load_env, model):
    db_path, dsl = load_env
    table_name = model._table_name

    with (
        conn_context(db_path) as sqlite_conn,
        closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn,
    ):
        pg_cur = pg_conn.cursor()
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute(f"SELECT * FROM {table_name};")
        while True:
            sqlite_row = sqlite_cur.fetchone()
            if not sqlite_row:
                break

            sqlite_conv_row = model(**dict(sqlite_row)).get_dict_with_converted_dates()

            pg_cur.execute(f"SELECT * FROM {table_name} WHERE id = '{sqlite_conv_row['id']}'")
            pg_row = pg_cur.fetchone()
            pg_conv_row = dict()
            for key, value in pg_row.items():
                if type(value) is datetime.datetime:
                    pg_conv_row[key] = value.timestamp()
                else:
                    pg_conv_row[key] = value
            assert sqlite_conv_row == pg_conv_row
