import sqlite3
from dataclasses import dataclass
import datetime

from sqlite_to_postgres.postgres import Postgres


class SQLite:
    def __init__(self, connection):
        self.connection = connection
        self.curs = self.connection.cursor()

    @staticmethod
    def transform_date(s):
        transformed_date = datetime.datetime.strptime(str(s, 'utf-8'), '%Y-%m-%d %H:%M:%S.%f+00')
        return transformed_date.replace(tzinfo=datetime.timezone.utc)

    def extract_data_and_save_to_postgres(self, pg_conn, table_name: str, model: dataclass, batch_size: int):
        sqlite3.register_converter('timestamp', self.transform_date)

        self.curs.execute(f"SELECT * FROM {table_name};")

        while True:
            batch_data = self.curs.fetchmany(size=batch_size)

            if not batch_data:
                break

            insert_data = [model(*data) for data in batch_data]

            Postgres(pg_conn=pg_conn).save_all_data(table_name=table_name, insert_data=insert_data)
