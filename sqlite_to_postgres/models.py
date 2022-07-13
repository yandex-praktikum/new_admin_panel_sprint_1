from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional
from uuid import UUID


class FilmType(str, Enum):
    movie = 'movie'
    tv_show = 'tv_show'


@dataclass
class UUIDMixin:
    id: UUID


@dataclass
class TimeStampedMixin:
    created: datetime
    modified: datetime


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    name: str
    description: Optional[str] = ""


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str


@dataclass
class Filmwork(UUIDMixin, TimeStampedMixin):
    title: str
    creation_date: date
    type: FilmType
    description: Optional[str] = ""
    # certificate: Optional[str] = None
    file_path: Optional[str] = None
    rating: float = field(default=0.0)


@dataclass
class GenreFilmwork(UUIDMixin):
    film_work_id: UUID
    genre_id: UUID
    created: datetime


@dataclass
class PersonFilmwork(UUIDMixin):
    film_work_id: UUID
    person_id: UUID
    role: str
    created: datetime
