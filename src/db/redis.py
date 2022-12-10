import hashlib
import logging
from typing import Optional

from aioredis import Redis

from db.cache import CacheInterface
from models.paginate import Pagination

# переменная хранит объект подключения после чего передачи
redis_conn: Optional[Redis] = None


async def get_cache_conn() -> Optional[Redis]:
    """Вернуть подключение к redis, если оно создано, иначе None."""
    return redis_conn


class RedisMixin(CacheInterface):
    """Реализация интерфейса кэша и работающая через redis."""

    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    async def get_cache(self, key: str) -> Optional[bytes]:
        """Получить запись из кэша по переданному ключу.
        Args:
            key: ключ
        Returns:
            Запись из кэша в формате bytes.
        """
        data = await self.redis.get(key)
        if data is not None:
            logging.info(f"got record from cache.")

        return data

    async def set_cache(self, key: str, data: bytes, expire: int = 60 * 5) -> None:
        """Создать запись в Redis по переданному ключу.
        Args:
            key: ключ, по которому будет создана запись.
            data: данные, которые будут записаны в кэш.
        Returns:
            None
        """
        await self.redis.set(key, data, ex=expire)
        logging.info("record in cache created.")

    async def create_key(
        self,
        params: list,
        sort: Optional[str] = "",
        index_name: Optional[str] = "",
        paginate: Optional[Pagination] = None,
    ) -> str:
        """создать ключ для запроса.
        Args:
            filter: поля фильтрации.
            sort: Поле сортировки.
        Returns:
            str: ключ для данного запроса.
        """
        data = index_name
        if isinstance(params, str):
            data = params
        else:
            params = list(filter(lambda param: param[1], params))
            for param in params:
                # if param[1]:
                data += str(param[1])

        if sort:
            data += sort
        if paginate is not None:
            data += str(paginate.number)
            data += str(paginate.size)
        key = data.encode("utf-8")

        return hashlib.md5(key).hexdigest()
