from elasticsearch import Elasticsearch

from logger import log
from my_dataclass import Movies
from utils import backoff


def elastic_connect(func):
    """Деккоратор для получения соединения с elasticsearch"""

    def wrapper(self, *args, **kwargs):
        el_search = self._get_connection()
        log.info("Connected to elasticsearch.")
        res = func(self, *args, el_search=el_search, **kwargs)
        return res

    return wrapper


class ElasticSearchLoader:
    """Класс для записии обновления данных в индекс elasticsearch"""

    def __init__(self, connect_url: str, index: dict, index_name: str) -> None:
        self.connect_url = connect_url
        self.index = index
        self.index_name = index_name
        self.created_index = False

    def _get_connection(self) -> Elasticsearch:
        el_search = Elasticsearch([self.connect_url])
        return el_search

    @backoff()
    @elastic_connect
    def load_data(self, dict_data: dict, el_search: Elasticsearch, index: str) -> None:
        """Метод для записи и обновления данных в Elasticsearch

        Args:
            dict_data : Пачка подготовленных данных для записи в индекс
            el_search (Elasticsearch): объект класса Elasticsearch
        """
        for data in dict_data:
            # не стал делать циклы на создание индекса, тк
            # 1. elastic автоматом должен создать идекс
            # 2. не хотел колхозить еще 1 цикл
            # if not self.created_index:
            #     el_search.indices.create(index=self.index_name, ignore=400,
            #                              body=self.index)
            #     self.created_index = True
            res = el_search.index(index=index, id=data["id"], body=data)
            log.info(res)
