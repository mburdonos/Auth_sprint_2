from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError

from db.database import DatabaseInterface
from models.paginate import Pagination

# переменная хранит объект подключения после чего передачи
es_conn: Optional[AsyncElasticsearch] = None


async def get_database_conn() -> Optional[AsyncElasticsearch]:
    """Вернуть подключение к elasticsearch, если оно создано, иначе None."""
    return es_conn


class ElasticMixin(DatabaseInterface):
    """Реализация интерфейса базы данных и работающая через elasticsearch."""

    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic: AsyncElasticsearch = elastic
        self.index_name: str

    async def get_record_from_db(self, id_: str) -> Optional[dict]:
        try:
            doc = await self.elastic.get(self.index_name, id_)
        except NotFoundError:
            return None
        doc = doc["_source"]

        return doc

    async def get_list_from_db(self, query: dict, sorter: list = []) -> list[dict]:
        result = await self.elastic.search(
            index=self.index_name, sort=sorter, body=query, request_timeout=90,
        )

        try:
            docs = result["hits"]["hits"]
        except KeyError:
            docs = []

        return docs

    async def create_query(self, paginate: Optional[Pagination], filters) -> dict:
        """Создать запрос в elaticsarch, основыванный на заднных фильтрах.
        Args:
            filters: Поля фильтрации.
        Returns:
            dict: составленный запрос.
        """
        request_body = {
            "size": paginate.size,
            "from": (paginate.number - 1) * paginate.size,
            "query": {},
        }
        if isinstance(filters, str):
            request_body["query"] = {
                "multi_match": {
                    "query": f"{filters}",
                    "type": "phrase",
                    "fields": ["*"],
                }
            }
        else:
            request_body["query"] = {"bool": {"must": []}}
            for filter_ in filters:
                if filter_[1]:
                    request_body["query"]["bool"]["must"].append(
                        {"match_phrase": {f"{filter_[0]}": f"{filter_[1]}"}}
                    )

        return request_body

    async def create_sorter(self, sort: str = "") -> list:
        """Преобразуем параметр сортировки к нужном формате.
        Args:
            sort: Поле сортировки.
        Returns:
            list: список полей сортировки.
        """
        if not sort:
            return []
        direct = "DESC" if sort.startswith("-") else "ASC"

        return [f"{sort.replace('-', '')}:{direct}"]
