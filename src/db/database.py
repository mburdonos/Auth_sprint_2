from abc import ABC, abstractmethod
from typing import Optional


class DatabaseInterface(ABC):
    """База данных предоставляет объекты и списки объектов."""

    @abstractmethod
    def get_record_from_db(self, id_: str, *args, **kwargs) -> Optional[dict]:
        """Получить документ из Elasticsearch по id."""
        pass

    @abstractmethod
    def get_list_from_db(self, query: dict, sorter: list = [], *args, **kwargs) -> list[dict]:
        """Получить список документов из Elasticsearch по заданным фильтрам."""
        pass
