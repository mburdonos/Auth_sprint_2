from typing import Optional

from .base_model import BaseModelMixin


class GenreList(BaseModelMixin):
    """Валидатор записи индекса 'genres' для списка."""

    name: str


class GenreDetails(BaseModelMixin):
    """Валидатор записи индекса 'genres' для объекта."""

    name: str
    film_ids: str
