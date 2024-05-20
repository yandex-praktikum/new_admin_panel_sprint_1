import dataclasses
import os
import pathlib
import sqlite3
from contextlib import closing, contextmanager
from itertools import count
from typing import Generator, Iterable

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_values

from sqlite_to_postgres.logger import logger
from sqlite_to_postgres.models import MODELS

BATCH_SIZE = 1000
CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
load_dotenv(str(CURRENT_DIR.parent.joinpath("movies_admin/config/.env")))


@contextmanager
def conn_context(db_path: str) -> Generator:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = pg_conn.cursor()

    @staticmethod
    def convert_data(model: "dataclasses.dataclass", data: Iterable) -> list:
        return list(map(lambda m: model(**dict(m)).dict(), data))

    def save_all_data(self, model: "dataclasses.dataclass", data: Iterable):
        data = self.convert_data(model, data)
        execute_values(
            self.cursor,
            f"INSERT INTO {model._table_name} "
            f"({', '.join(model.get_alias_field_names())}) VALUES %s"
            f"ON CONFLICT (id) DO UPDATE SET "
            f"{model.make_exclusion()}",
            argslist=data,
            template=model.get_template(),
        )


class SQLiteExtractor:
    def __init__(self, sqlite_conn: sqlite3.Connection):
        self.cursor = sqlite_conn.cursor()

    def extract_data(self, model: "dataclasses.dataclass") -> Generator:
        c = count(1)
        self.cursor.execute(f"SELECT * FROM {model._table_name};")
        while True:
            results = self.cursor.fetchmany(BATCH_SIZE)
            logger.info(f"Inserting batch #{next(c)}")
            if not results:
                break
            yield results


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    for model in MODELS:
        table_name = model._table_name
        logger.info(f"Migrate data from table {table_name}")
        data = sqlite_extractor.extract_data(model)
        for item in data:
            postgres_saver.save_all_data(model, item)


if __name__ == "__main__":
    db_path = os.environ.get("SQLITE_BASE", "db.sqlite")
    dsl = {
        "dbname": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": os.environ.get("DB_PORT", 5432),
        "options": f'-c search_path={os.environ.get("SCHEMA")}',
    }

    with (
        conn_context(db_path) as sqlite_conn,
        closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn,
    ):
        load_from_sqlite(sqlite_conn, pg_conn)
