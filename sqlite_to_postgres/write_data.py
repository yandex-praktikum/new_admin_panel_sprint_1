from psycopg2.extensions import connection as _connection


class PostgresSaver():
    def __init__(self, pg_conn: _connection) -> None:
        self.pg_conn = pg_conn
        self.tables = None