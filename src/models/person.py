from typing import Optional

from pydantic import BaseModel

from .base_model import BaseModelMixin


class FilmId(BaseModel):
    """Валидатор для вложенного поля с персонами."""

    actors: Optional[str]
    directors: Optional[str]
    writers: Optional[str]


class PersonList(BaseModelMixin):
    """Валидатор записи индекса 'persons' для списка."""

    full_name: str


class PersonDetails(BaseModelMixin):
    """Валидатор записи индекса 'persons' для объекта."""

    full_name: str
    film_ids: FilmId
