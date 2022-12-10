import random
import uuid

from models.film import FilmDetails
from models.genre import GenreDetails
from models.person import FilmId, PersonDetails


async def generate_films(i: int) -> dict:
    return FilmDetails(
        id=str(uuid.uuid4()),
        title="The Star" + str(i),
        imdb_rating=random.randrange(1, 10),
        description="New World",
        genre=["Action" + str(i), "Sci-Fi" + str(i)],
        actors_names=["Ann", "Bob" + str(i)],
        writers_names=["Ben" + str(i), "Howard" + str(i)],
    ).dict()


async def generate_genre(i: int) -> dict:
    return GenreDetails(
        id=str(uuid.uuid4()),
        name="John Johnch" + str(i),
        film_ids=str(uuid.uuid4()) + "," + str(uuid.uuid4()),
    ).dict()


async def generate_person(i: int) -> dict:
    return PersonDetails(
        id=str(uuid.uuid4()),
        full_name="John Johnch" + str(i),
        film_ids=FilmId(
            actors=str(uuid.uuid4()) + "," + str(uuid.uuid4()),
            directors=str(uuid.uuid4()) + "," + str(uuid.uuid4()),
            writers=str(uuid.uuid4()) + "," + str(uuid.uuid4()),
        ),
    ).dict()
