import os
from pathlib import Path

from dotenv import load_dotenv

from state_storage import JsonFileStorage, StateFile

load_dotenv()
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Количество записей в пачке
LIMIT = 5000

# Время ожидания, если обновленных даписей нет
WAITING_TIME = 10

# настройки для подключения к БД
DSL = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Имена используемых таблиц
# структура: таблица -> к ней может быть несколько запросов,
# где результат запроса должен быть записан в соответствующий класс
TABLES = {
     "film_work": {"film_work": "Movies",
                   "person_film_work": "PersonMovies",
                   "genre_film_work": "GenreMovies"},
    "person": {"person": "Movies", "person_person": "PersonMovies"},
     "genre": {"genre": "Movies", "genre_genre": "GenreMovies"},
}

# Настройки для подключения к elastic
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")

# Путь к файлу с настройками индекса
INDEX_FILE_PATH = os.getenv("INDEX_FILE_PATH")

# Имя индекса
INDEX_NAME = os.getenv("INDEX_NAME")

storage = JsonFileStorage(INDEX_FILE_PATH)
state_storage = StateFile(storage)

# Настройки индекса
INDEX = state_storage.get_state("index")

# Шаблон файла для хранения обновленных данных
STORING_UPDATE_DATE = os.getenv("STORING_UPDATE_DATE")

# Шаблон файла для хранения даты обновления
STORING_TABLE_DATA = os.getenv("STORING_TABLE_DATA")
