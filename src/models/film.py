from typing import Optional

from .base_model import BaseModelMixin


class FilmList(BaseModelMixin):
    """Валидатор записи индекса 'movies' для списка."""

    title: str
    imdb_rating: float


class FilmDetails(BaseModelMixin):
    """Валидатор записи индекса 'movies' для объекта."""

    title: str
    imdb_rating: float
    description: str
    genre: list
    actors_names: list
    writers_names: list
