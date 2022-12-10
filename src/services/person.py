from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.cache import CacheInterface
from db.database import DatabaseInterface
from db.elastic import get_database_conn
from db.redis import get_cache_conn
from models.paginate import Pagination
from models.person import PersonDetails, PersonList
from services.base_service import BaseServiceMixin


class PersonService(BaseServiceMixin):
    """Сервис, обеспечивающий работу с эндпоинтами персон."""

    def __init__(self, cache_conn: CacheInterface, database_conn: DatabaseInterface):
        super().__init__(cache_conn, database_conn)
        self.index_name = "person_movies"

    async def get_obj(self, id_: str) -> Optional[PersonDetails]:
        doc = await self.get_doc(id_)
        if not doc:
            return None

        return PersonDetails(**doc)

    async def get_obj_list(
        self, filters, paginate: Optional[Pagination]
    ) -> list[PersonList]:
        docs = await self.get_docs_list(
            filters=filters, paginate=paginate, index_name=self.index_name
        )

        return [PersonList(**doc["_source"]) for doc in docs]


@lru_cache()
def get_person_service(
    cache_conn: CacheInterface = Depends(get_cache_conn),
    database_conn: DatabaseInterface = Depends(get_database_conn),
) -> PersonService:
    return PersonService(cache_conn, database_conn)
