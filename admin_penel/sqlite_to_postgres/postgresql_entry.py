import sys
import traceback
from dataclasses import astuple

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
from settings import error_log, log


class PostgresSaver:
    """Класс для записи данных в postgres"""
    def __init__(self, conn: _connection, limit: int):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.conn.autocommit = True
        self.limit = limit

    def save_all_data(self, query: str, data: list, message: str = None):
        """Метод для записи данных в postgres

        Args:
            query (str): SQL-запрос для записи в таблицу
            data (list): список обхектов датакласса для записи
            message (str, optional): сообщение. Defaults to None.
        """
        try:
            data = [astuple(i) for i in data]
            execute_batch(self.cur, query, data, page_size=self.limit)
            log.info(message)

        except psycopg2.Error as err:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_no = str(frame[0]).split()[4]
            error_log(line_no)
            raise err
