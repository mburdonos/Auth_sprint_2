import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from my_dataclasses import (FilmWork, Genre, GenreFilmWork, Person,
                            PersonFilmWork)
from psycopg2.extras import DictCursor

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@contextmanager
def psql_conn_context(connect_data: dict):
    conn = psycopg2.connect(**connect_data, cursor_factory=DictCursor)
    yield conn
    cur = conn.cursor()
    cur.close()
    conn.close()


LIMIT = 10

DB_PATH = os.getenv("DB_PATH")

DSL = {
        'dbname': os.getenv("POSTGRES_DB"),
        'user': os.getenv("POSTGRES_USER"),
        'password': os.getenv("POSTGRES_PASSWORD"),
        'host': os.getenv("POSTGRES_HOST"),
        'port': os.getenv("POSTGRES_PORT")
        }

DATABASE_QUERIES = [
    {
        'read_data': 'SELECT id, name, description FROM genre',
        'save_data': 'INSERT INTO content.genre (name, '
                     + 'description, id, created, modified) VALUES '
                     + '(%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;',
        'dataclass': Genre
    },
    {
        'read_data': 'SELECT id, title, description, creation_date,'
                     + ' rating, type FROM film_work',
        'save_data': 'INSERT INTO content.film_work (title, description, '
                     + 'creation_date, type, rating, '
                     + 'id, created, modified) VALUES '
                     + '(%s, %s, %s, %s, %s, %s, %s, %s) '
                     + 'ON CONFLICT (id) DO NOTHING;',
        'dataclass': FilmWork
    },
    {
        'read_data': 'SELECT id, film_work_id, genre_id FROM genre_film_work',
        'save_data': 'INSERT INTO content.genre_film_work (id, film_work_id, '
                     + 'genre_id, created) VALUES (%s, %s, %s, %s) ON CONFLICT'
                     + ' (id) DO NOTHING;',
        'dataclass': GenreFilmWork
    },
    {
        'read_data': 'SELECT id, full_name FROM person',
        'save_data': 'INSERT INTO content.person (full_name, id, created, '
                     + 'modified) VALUES (%s, %s, %s, %s) ON CONFLICT (id) '
                     + 'DO NOTHING;',
        'dataclass': Person
    },
    {
        'read_data': 'SELECT id, role, film_work_id, person_id FROM '
                     + 'person_film_work',
        'save_data': 'INSERT INTO content.person_film_work (role, id, '
                     + 'film_work_id, person_id, created) VALUES '
                     + '(%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;',
        'dataclass': PersonFilmWork
    },
]
