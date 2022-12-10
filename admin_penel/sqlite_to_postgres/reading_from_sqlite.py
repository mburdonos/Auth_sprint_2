import sqlite3
import sys
import traceback

from settings import error_log


class SQLiteLoader():
    """Класс для чтения данных из sqlite"""
    def __init__(self, connection: sqlite3.Connection, limit: int) -> None:
        self.curs = connection.cursor()
        self.limit = limit
        self.count = 0

    def get_objects_from_table(self, qeryset: str):
        """Метод для получения списка полей из таблицы

        Args:
            qeryset (str): Запрос для выборки данных

        Returns:
            list: список с записями из таблицы
        """
        self.curs.execute(f"{qeryset} LIMIT {self.count},{self.limit};")
        data = [dict(i) for i in self.curs.fetchall()]
        if not data:
            return None
        return data

    def load_data(self, qeryset: str, dataclass):
        """Метод выгрузки готовых пачек записи из таблицы

        Args:
            qeryset (str): Запрос для выборки данных
            dataclass (dataclass): Датакласс для записи полей из таблицы

        Yields:
            list: список с объектами полученного датакласса
        """
        try:
            while True:
                data = self.get_objects_from_table(qeryset)
                self.count += self.limit
                if data:
                    yield [dataclass(**i) for i in data]
                else:
                    break
        except sqlite3.Error as err:
            frame = traceback.extract_tb(sys.exc_info()[2])
            line_no = str(frame[0]).split()[4]
            error_log(line_no)
            raise err
