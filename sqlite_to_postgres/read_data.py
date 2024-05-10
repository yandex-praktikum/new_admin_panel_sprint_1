import sqlite3
import uuid

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Genre:
    name: str
    created_at: datetime
    updated_at: datetime
    description: str = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Film_work:
    title: str
    type: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    description: str = field(default=None)
    creation_date: datetime = field(default=None)
    file_path: str = field(default=None)
    rating: float = field(default=0.0)


@dataclass
class Person:
    full_name: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre_film_work:
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person_film_work:
    role: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)


class SQLiteExtractor():

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.sl_conn = connection
        self.lines = 50

    def extract_movies(self) -> dict:
        tables = ['genre', 'film_work', 'person', 'genre_film_work',
                  'person_film_work']

        for table in tables:
            # if table != 'person_film_work':
            #     continue
            curs = self.sl_conn.cursor()
            curs.execute(f"SELECT * FROM {table};")
            data = curs.fetchall()
            # print(dict(data[0]))

            if table == 'genre':
                load_genre = [Genre(**dict(_)) for _ in data]
            elif table == 'film_work':
                load_genre = [Film_work(**dict(_)) for _ in data]
            elif table == 'person':
                load_genre = [Person(**dict(_)) for _ in data]
            elif table == 'genre_film_work':
                load_genre = [Genre_film_work(**dict(_)) for _ in data]
            elif table == 'person_film_work':
                load_genre = [Person_film_work(**dict(_)) for _ in data]
            else:
                load_genre = []

            for fix_data in list(range(0, len(load_genre), self.lines)):
                yield {'table': table,
                       'data': load_genre[fix_data:fix_data+self.lines]}
