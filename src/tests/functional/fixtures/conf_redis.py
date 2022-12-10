import hashlib
from typing import Optional

import backoff
import pytest_asyncio
import requests
from redis import asyncio as aioredis

from tests.functional.settings import test_settings


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
@pytest_asyncio.fixture(scope="session")
async def redis_client():
    client_redis = await aioredis.Redis(
        host=test_settings.redis_host, port=test_settings.redis_port
    )
    yield client_redis
    await client_redis.close()


@pytest_asyncio.fixture
async def get_data(redis_client):
    async def inner(key: str) -> Optional[str]:
        data = await redis_client.get(key)
        if not data:
            return None

        return data

    return inner


@pytest_asyncio.fixture
def set_data(redis_client):
    async def inner(key: str, data: str):
        await redis_client.set(name=key, value=data, ex=10)

    return inner


@pytest_asyncio.fixture
def create_key():
    async def inner(params: list, api: str) -> str:
        """создает ключ для запроса.
          Args:
              filter: поля фильтрации.
              sort: Поле сортировки.
          Returns:
              str: ключ для данного запроса.
          """
        data = api
        for param in params:
            if params[param]:
                data += str(params[param])
        key = data.encode("utf-8")
        return hashlib.md5(key).hexdigest()

    return inner
