from abc import ABC, abstractmethod
from typing import Optional

import orjson
from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from db.elastic import ElasticMixin
from db.redis import RedisMixin
from models.base_model import BaseModelMixin
from models.paginate import Pagination


class BaseServiceInterface(ABC):
    """Базовый интерфейс для сервисов."""

    @abstractmethod
    def get_obj(self, id_: str) -> BaseModelMixin:
        """Получить объект по id."""
        pass

    @abstractmethod
    def get_obj_list(self, filters: list, sort: str = "") -> list[BaseModelMixin]:
        """Получить список объектов по заданным фильтрам."""
        pass


class BaseServiceMixin(BaseServiceInterface, RedisMixin, ElasticMixin):
    """Миксин, реализующий основную логику сервисов."""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        RedisMixin.__init__(self, redis)
        ElasticMixin.__init__(self, elastic)

    async def get_doc(self, id_: str) -> Optional[dict]:
        """Получить документ из Redis или Elasticsearch по id."""
        doc = await self.get_cache(id_)
        if doc is None:
            doc = await self.get_record_from_db(id_)
            if doc is not None:
                await self.set_cache(doc["id"], orjson.dumps(doc))
        else:
            doc = orjson.loads(doc)

        return doc

    async def get_docs_list(
        self,
        filters,
        paginate: Optional[Pagination],
        sort: str = "",
        index_name: str = "",
    ) -> list[dict]:
        """Получить список документов из Redis или Elasticsearch по заданным фильтрам."""
        query = await self.create_query(paginate=paginate, filters=filters)
        sorter = await self.create_sorter(sort)
        key = await self.create_key(filters, sort, index_name, paginate)

        docs = await self.get_cache(key)
        if docs is None:
            docs = await self.get_list_from_db(query, sorter)
            await self.set_cache(key, orjson.dumps(docs))
        else:
            docs = orjson.loads(docs)

        return docs
