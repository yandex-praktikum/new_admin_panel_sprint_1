import collections.abc as collections_abc
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, Any

import psycopg2.extensions as psycopg2_extensions


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


ConnectionSqlite = sqlite3.Connection
ConnectionPsycopg = psycopg2_extensions.connection
