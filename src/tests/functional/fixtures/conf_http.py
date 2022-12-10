import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture(scope="session")
async def http_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(http_client):
    async def inner(url_start, query_data):
        response = await http_client.get(url_start, params=query_data)
        return response

    return inner
