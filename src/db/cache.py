from abc import ABC, abstractmethod
from typing import Optional


class CacheInterface(ABC):
    """Система кэша должна создавать и извлекать записи с данными по заданному ключу."""

    @abstractmethod
    def get_cache(self, key: str, *args, **kwargs) -> Optional[bytes]:
        pass

    @abstractmethod
    def set_cache(self, key: str, data: bytes, expire: int, *args, **kwargs) -> None:
        pass
