import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
async def http_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(http_client):
    async def inner(url_start, query_data=None):
        response = await http_client.get(url_start, params=query_data)
        return response

    return inner


@pytest_asyncio.fixture
def make_post_request(http_client):
    async def inner(url_start, query_data, **kwargs):
        response = await http_client.post(url_start, data=query_data, **kwargs)
        return response

    return inner


@pytest_asyncio.fixture()
async def number(i=0):
    return i + 1
