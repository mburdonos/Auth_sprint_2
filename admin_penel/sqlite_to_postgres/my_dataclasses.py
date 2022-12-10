import uuid
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class FilmWork:
    """Класс для хранения данных из таблицы film_work"""
    title: str
    description: str
    creation_date: str
    type: str
    rating: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
    modified: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.title = self.title or 'Без названия'
        self.description = self.description or 'Нет описания'
        self.creation_date = datetime.strptime(
            self.creation_date, '%Y-%m-%d'
        ).date() if self.creation_date else date.today()
        self.type = self.type or 'movie'
        self.rating = self.rating or 0.0
        self.created = self.created or datetime.utcnow()
        self.modified = self.modified or datetime.utcnow()


@dataclass
class Person:
    """Класс для хранения данных из таблицы person"""
    full_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
    modified: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.full_name = self.full_name or 'Какой-то ноунейм'
        self.created = self.created or datetime.utcnow()
        self.modified = self.modified or datetime.utcnow()


@dataclass
class PersonFilmWork:
    """Класс для хранения данных из таблицы person_film_work"""
    role: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.role = self.role or 'Неизвестно'
        self.created = self.created or datetime.utcnow()


@dataclass
class Genre:
    """Класс для хранения данных из таблицы genre"""
    name: str
    description: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
    modified: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.name = self.name or 'Без названия'
        self.description = self.description or 'Без описания'
        self.created = self.created or datetime.utcnow()
        self.modified = self.modified or datetime.utcnow()


@dataclass
class GenreFilmWork:
    """Класс для хранения данных из таблицы genre_film_work"""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.created = self.created or datetime.utcnow()
