import sqlite3
from dataclasses import dataclass
import datetime


class SQLite:
    def __init__(self, connection):
        self.connection = connection

    def extract_data(self, table_name: str, model: dataclass) -> list:
        def transform_date(s):
            transformed_date = datetime.datetime.strptime(str(s, 'utf-8'), '%Y-%m-%d %H:%M:%S.%f+00')
            return transformed_date.replace(tzinfo=datetime.timezone.utc)

        sqlite3.register_converter('timestamp', transform_date)

        curs = self.connection.cursor()
        curs.execute(f"SELECT * FROM {table_name};")
        all_data = curs.fetchall()

        return [model(*data) for data in all_data]
