import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Movies:
    """Класс для хранения данных по фильму"""

    title: str
    description: str
    type: str
    persons: list
    rating: float
    genres: list
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
    modified: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.created = str(self.created)
        self.modified = str(self.modified)

    def _get_names_by_role(self, role: str) -> str:
        name_list = [i["person_name"] for i in self.persons if i["person_role"] == role]
        return " ".join(name_list) or ""

    def _get_data_persons(self, role: str) -> list:
        persons_data = []
        for person in self.persons:
            if person["person_role"] == role:
                person_data = {
                    "id": person["person_id"],
                    "name": person["person_name"],
                }
                persons_data.append(person_data)
        return persons_data

    def as_dict(self) -> dict:
        """Метод подготовки данных к записи в индекс elastic

        Returns:
            dict: словарь подготовленных данных
        """
        movies_data = {
            "id": self.id,
            "imdb_rating": self.rating,
            "genre": " ".join(self.genres) if None is self.genres else "",
            "title": self.title,
            "description": self.description,
            "director": self._get_names_by_role("director"),
            "actors_names": self._get_names_by_role("actor"),
            "writers_names": self._get_names_by_role("writer"),
            "actors": self._get_data_persons("actor"),
            "writers": self._get_data_persons("writer"),
        }
        return movies_data


@dataclass
class PersonMovies:
    """Класс для хранения данных по персонам"""

    full_name: str
    actors: list
    writers: list
    directors: list
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
    modified: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.created = str(self.created)
        self.modified = str(self.modified)

    def as_dict(self) -> dict:
        """Метод подготовки данных к записи в индекс elastic

        Returns:
            dict: словарь подготовленных данных
        """
        movies_data = {
            "id": self.id,
            "full_name": self.full_name,
            "film_ids": {
                "actors": self.actors,
                "writers": self.writers,
                "directors": self.directors,
            },
        }
        return movies_data


@dataclass
class GenreMovies:
    """Класс для хранения данных по персонам"""

    name: str
    film_ids: list
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
    modified: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.created = str(self.created)
        self.modified = str(self.modified)

    def as_dict(self) -> dict:
        """Метод подготовки данных к записи в индекс elastic

        Returns:
            dict: словарь подготовленных данных
        """
        movies_data = {
            "id": self.id,
            "name": self.name,
            "film_ids": self.film_ids,
        }
        return movies_data
