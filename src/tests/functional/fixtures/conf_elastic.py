import json
from typing import List

import backoff
import pytest_asyncio
import requests
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import test_settings


async def delete_index(client):
    index_list = await client.indices.get(index="*")
    for index in index_list:
        if not index.startswith("."):
            await client.indices.delete(index=index)


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await delete_index(client)
    await client.close()


async def get_es_bulk_query(data: List[dict], es_index: str, es_id_field: str) -> List:
    bulk_query = []
    for row in data:
        bulk_query.extend(
            [
                json.dumps({"index": {"_index": es_index, "_id": row[es_id_field]}}),
                json.dumps(row),
            ]
        )
    return bulk_query


@pytest_asyncio.fixture
def es_write_data(es_client):
    async def inner(data: List[dict], es_index: str, es_id_field):
        bulk_query = await get_es_bulk_query(data, es_index, es_id_field)
        str_query = "\n".join(bulk_query) + "\n"
        response = await es_client.bulk(str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner
