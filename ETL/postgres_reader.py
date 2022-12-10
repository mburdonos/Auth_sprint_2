import psycopg2
from psycopg2.extras import DictCursor

from logger import log
from utils import backoff


def psql_connect(func):
    """Деккоратор для получения соединения с postgresql."""
    def wrapper(self, *args, **kwargs):
        # Получаем соединение и курсор
        cursor = self._get_connection().cursor()
        log.info('Connected to postgresql.')
        # Передаем его в декарируемую функцию
        res = func(self, *args, cursor=cursor, **kwargs)
        # Делаем коммит и закрываем соединение
        self._get_connection().commit()
        cursor.close()
        return res
    return wrapper


class PostgresReader:
    def __init__(self, connect_data: dict, limit: int):
        self.limit = limit
        self.connect_data = connect_data
        self.connection = None

    def __del__(self):
        if self.connection:
            self.connection.close()

    def _get_connection(self):
        if not self.connection:
            self.connection = psycopg2.connect(**self.connect_data,
                                               cursor_factory=DictCursor)
        return self.connection

    @backoff()
    @psql_connect
    def get_data(self, qeryset: str, cursor):
        """Получает данные из postgres"""
        cursor.execute(qeryset)
        data = [dict(i) for i in cursor.fetchall()]
        return data

    @backoff()
    @psql_connect
    def extract_data_from(self, qeryset: str, time_update, cursor):
        """Получает данные из postgres для конкретного времени обновления"""
        qeryset = qeryset.format(time_update) + f' LIMIT {self.limit};'
        cursor.execute(qeryset)
        rows = [dict(i) for i in cursor.fetchall()]
        return rows
