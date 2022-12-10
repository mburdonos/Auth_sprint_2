import pytest_asyncio

from tests.functional.testdata.generate_data import (
    generate_films,
    generate_genre,
    generate_person,
)


@pytest_asyncio.fixture(scope="session")
async def es_data_film():
    data = [await generate_films(_) for _ in range(60)]
    return data


@pytest_asyncio.fixture(scope="session")
async def es_data_person():
    data = [await generate_person(_) for _ in range(60)]
    return data


@pytest_asyncio.fixture(scope="session")
async def es_data_genre():
    data = [await generate_genre(_) for _ in range(60)]
    return data
