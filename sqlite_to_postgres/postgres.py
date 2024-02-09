from dataclasses import astuple, fields, dataclass


class Postgres:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn
        self.curs = self.pg_conn.cursor()

    def save_all_data(self, table_name: str, insert_data: list):
        column_names = [field.name for field in fields(insert_data[0])]
        column_names_str = ','.join(column_names)

        col_count = ', '.join(['%s'] * len(column_names))

        bind_values = ','.join(
            self.curs.mogrify(f"({col_count})", astuple(data)).decode('utf-8') for data in insert_data
        )
        query = f'''
            INSERT INTO content.{table_name} ({column_names_str}) 
            VALUES {bind_values} ON CONFLICT (id) DO NOTHING
        '''

        self.curs.execute(query)

    def get_all_data(self, table_name: str, model: dataclass):
        query = f'SELECT * from content.{table_name};'
        self.curs.execute(query)
        all_data = self.curs.fetchall()
        return [model(*data) for data in all_data]
