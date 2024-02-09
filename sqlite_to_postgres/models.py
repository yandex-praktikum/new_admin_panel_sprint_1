from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class FilmWork:
    id: uuid4
    title: str
    description: str
    creation_date: datetime
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre:
    id: uuid4
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilmWork:
    id: uuid4
    film_work_id: uuid4
    genre_id: uuid4
    created_at: datetime


@dataclass
class Person:
    id: uuid4
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class PersonFilmWork:
    id: uuid4
    film_work_id: uuid4
    person_id: uuid4
    role: str
    created_at: datetime
