from functools import lru_cache
from typing import Optional

from fastapi import Depends

from db.cache import CacheInterface
from db.database import DatabaseInterface
from db.elastic import get_database_conn
from db.redis import get_cache_conn
from models.film import FilmDetails, FilmList
from models.paginate import Pagination
from services.base_service import BaseServiceMixin


class FilmService(BaseServiceMixin):
    """Сервис, обеспечивающий работу с эндпоинтами фильмов."""

    def __init__(self, cache_conn: CacheInterface, database_conn: DatabaseInterface):
        super().__init__(cache_conn, database_conn)
        self.index_name = "movies"

    async def get_obj(self, id_: str) -> Optional[FilmDetails]:
        doc = await self.get_doc(id_)
        if not doc:
            return None

        return FilmDetails(**doc)

    async def get_obj_list(
        self, filters, paginate: Optional[Pagination], sort: str = ""
    ) -> list[FilmList]:
        docs = await self.get_docs_list(filters, paginate, sort, self.index_name)

        return [FilmList(**doc["_source"]) for doc in docs]


@lru_cache()
def get_film_service(
    cache_conn: CacheInterface = Depends(get_cache_conn),
    database_conn: DatabaseInterface = Depends(get_database_conn),
) -> FilmService:
    return FilmService(cache_conn, database_conn)
