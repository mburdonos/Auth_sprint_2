import backoff
import requests
from redis import asyncio as aioredis

from tests.functional.settings import test_settings


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
def redis_client():
    redis_client = aioredis.Redis(
        host=test_settings.redis_host,
        port=test_settings.redis_host,
        decode_responses=True,
    )
    return redis_client
