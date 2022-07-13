import collections.abc as collections_abc
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, List, TypeVar
from typing import Optional, Any

import psycopg2.extensions as psycopg2_extensions
from dateutil.parser import parse


# Не удалось нормально импортировать зависимости из
# sqlite_to_postgres/iterator.py, тк при запуске тестов
# не удается установить путь до модуля utils (из-за разных
# путей запуска питона). Лучшее решение: во всех скриптах
# по умолчанию выставлять корневой папкой путь проекта -
# new_admin_panel_sprint_1. И уже везде прописать правильные пути.

@contextmanager
def sqlite_conn_context(
        db_path: str
) -> collections_abc.Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


@dataclass
class PipelineElement:
    table: str
    model: Any
    fields_to_rename: Optional[dict] = None
    skip_empty_fields: Optional[list] = None


def load_db_envs():
    envs = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    return envs


def convert_timestamp(raw_datetime: str):
    return parse(raw_datetime)


ConnectionSqlite = sqlite3.Connection
ConnectionPsycopg = psycopg2_extensions.connection

sqlite3.register_converter("timestamp", convert_timestamp)
sqlite3.register_converter("timestam", convert_timestamp)

T = TypeVar("T")


class Iterator:
    def __init__(self, connection: ConnectionSqlite):
        self.connection = connection

    @staticmethod
    def get_field_names_from_cursor(
            curs,
            fields_to_rename: Dict[str, str] = None
    ) -> List[str]:
        field_names = []

        for e in curs.description:
            temp_name = e[0]

            if fields_to_rename and temp_name in fields_to_rename:
                temp_name = fields_to_rename[temp_name]

            field_names.append(temp_name)

        return field_names

    def make_table_iterable(
            self,
            fields_to_rename: Dict[str, str],
            query: str
    ):
        curs = self.connection.cursor()
        curs.execute(query)

        field_names = self.get_field_names_from_cursor(
            curs=curs,
            fields_to_rename=fields_to_rename
        )

        while execute := curs.fetchone():
            yield {field_names[e]: execute[e] for e in range(len(execute))}


def iter_table_chunked(
        p: PipelineElement,
        iterator: Iterator,
        query: str,
        chunk_size: int = 50
):
    elements = []

    for i in iterator.make_table_iterable(
            fields_to_rename=p.fields_to_rename,
            query=query
    ):
        if p.skip_empty_fields and set(p.skip_empty_fields) <= set(i.keys()):
            for f in p.skip_empty_fields:
                del i[f]

        element = p.model(**i)
        elements.append(element)

        if len(elements) >= chunk_size:
            yield elements
            elements.clear()

    yield elements
