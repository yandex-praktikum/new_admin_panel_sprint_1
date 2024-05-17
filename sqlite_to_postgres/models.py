import dataclasses
import datetime
import uuid
from typing import Optional


class DataClassWithAlias:
    def dict(self) -> dict:
        dict_map = {}
        for key, field in self.__dataclass_fields__.items():
            dict_map[key] = {
                "key": field.metadata.get("alias") or key,
                "inline": True if field.type.__dict__.get("__dataclass_params__") else False,
                "type": field.type,
            }
        return {
            dict_map[key]["key"]: (
                value if not dict_map[key]["inline"] else dict_map[key]["type"](**value).dict()
            )
            for key, value in self.__dict__.items()
        }

    def get_dict_with_converted_dates(self):
        result = dict()
        for key, value in self.dict().items():
            if key in ("created_at", "created", "updated", "updated_at", "modified"):
                v = datetime.datetime.strptime(value + "00", "%Y-%m-%d %H:%M:%S.%f%z").timestamp()
                result[key] = v
            else:
                result[key] = value
        return result

    @classmethod
    def get_original_field_names(cls):
        return tuple(cls.__dataclass_fields__.keys())

    @classmethod
    def get_alias_field_names(cls):
        fields = list()
        for key, field in cls.__dataclass_fields__.items():
            fields.append(field.metadata.get("alias") or key)
        return tuple(fields)

    @classmethod
    def get_template(cls):
        return "(" + ",".join(map(lambda m: f"%({m})s", cls.get_alias_field_names())) + ")"

    @classmethod
    def make_exclusion(cls):
        return ", ".join(map(lambda m: f"{m}=EXCLUDED.{m}", cls.get_alias_field_names()))


@dataclasses.dataclass
class TimeStampedMixin(DataClassWithAlias):
    created_at: datetime.datetime = dataclasses.field(metadata={"alias": "created"})
    updated_at: datetime.datetime = dataclasses.field(metadata={"alias": "modified"})


@dataclasses.dataclass
class Genre(TimeStampedMixin):
    id: uuid.UUID
    name: str
    description: Optional[str]

    _table_name = "genre"


@dataclasses.dataclass
class Person(TimeStampedMixin):
    id: uuid.UUID
    full_name: str

    _table_name = "person"


@dataclasses.dataclass
class Filmwork(TimeStampedMixin):
    id: uuid.UUID
    title: str
    description: Optional[str]
    creation_date: Optional[datetime.datetime]
    file_path: Optional[str]
    rating: float
    type: str

    _table_name = "film_work"


@dataclasses.dataclass
class GenreFilmwork(DataClassWithAlias):
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.datetime = dataclasses.field(metadata={"alias": "created"})

    _table_name = "genre_film_work"


@dataclasses.dataclass
class PersonFilmwork(DataClassWithAlias):
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.datetime = dataclasses.field(metadata={"alias": "created"})

    _table_name = "person_film_work"


MODELS = (Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork)
