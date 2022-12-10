from abc import ABCMeta, abstractmethod
from dataclasses import asdict
from datetime import datetime
from time import sleep
from typing import Any

from load import ElasticSearchLoader
from logger import log
from my_dataclass import Movies, PersonMovies, GenreMovies
from postgres_reader import PostgresReader
from state_storage import JsonFileStorage, StateFile

# в зависимости от типа данных поределяем
# какой класс определить и в какой индекс писать
compare = {
    "Movies": {"dataclass": Movies, "index": "movies"},
    "PersonMovies": {"dataclass": PersonMovies, "index": "person_movies"},
    "GenreMovies": {"dataclass": GenreMovies, "index": "genre_movies"},
}


class State(metaclass=ABCMeta):
    """Базовый класс для отдельных состояний"""

    def save_data_from_storage(
        self, data: dict, table: str, key: str, file_template: str
    ) -> None:
        """Сохраняет данные в файл

        Args:
            data (dict): словарь для сохранения
            table (str): Имя таблицы (для формирования имени файла)
            key (str): ключ для сохранения
            file_template (str): шаблон имени файла для сохранения
        """
        storage = JsonFileStorage(file_template.format(table))
        state_storage = StateFile(storage)
        state_storage.set_state(key, data)

    def get_data_from_storage(self, table: str, key: str, file_template: str) -> Any:
        """Получает данные из файла

        Args:
            table (str): Имя таблицы (для поиска нежного файла)
            key (str): ключ по которому надо вытащить данные из json
            file_template (str): шаблон имени файла

        Returns:
            Any: словарь или None если файла нет
        """
        storage = JsonFileStorage(file_template.format(table))
        state_storage = StateFile(storage)
        date = state_storage.get_state(key)
        return date

    @abstractmethod
    def run(self):
        pass


class Init(State):
    """
    Стартовое состояние программы. Записывает самую новую дату обновления из
    таблиц person и genre для исключения их из проверки при первом полном
    переносе всех данных
    """

    def __init__(self, etl, postgres: PostgresReader) -> None:
        """инит метод

        Args:
            etl (main.ETL): Объект управляющего класса состояниями
            postgres (PostgresReader): Объект класса PostgresReader
        """
        self.etl = etl
        self.reader = postgres

    def get_modified_date_for(self, table: str) -> dict:
        """Получает крайную дату обновления записи для указанной таблицы

        Args:
            table (str): Имя таблицы

        Returns:
            dict: словарик с датой обновления
        """
        qery = self.etl.queries.GET_MODIFIED_DATE.format(table)
        update = self.reader.get_data(qery)
        update[0]["modified"] = str(update[0]["modified"])
        return update[0]

    def run(self) -> None:
        """Метод запуска состояния - Получает крайнюю дату обновления записи
        для таблиц genre и person. Состояние включается 1 раз при старте -
        нужно для того, чтобы не записывать даные по вышеуказанным таблицам в
        случае если elastic пуст
        """
        # for table in list(self.etl.config.TABLES.keys()):
        #     date = self.get_modified_date_for(table)
        #     self.save_data_from_storage(
        #         date, table, "update", self.etl.config.STORING_UPDATE_DATE
        #     )

        log.info("Первичное остояние отработало успешно.")

        self.etl.state = self.etl.extract
        self.etl.run_state()


class Extract(State):
    """Состояние выгрузуи информации о фильмах из постгресс"""

    def __init__(self, etl, postgres: PostgresReader) -> None:
        """инит метод

        Args:
            etl (main.ETL): Объект управляющего класса состояниями
            postgres (PostgresReader): Объект класса PostgresReader
        """
        self.etl = etl
        self.reader = postgres

    def convert_to_dict(self, data: list, dataclass: Movies) -> list:
        """Перевод сырых данных из postgres в объекты датакалсса

        Args:
            data (list): сырые данные из postgres
            dataclass (Movies): датакласс

        Returns:
            list: список объектов датакласса
        """
        obj_data = [dataclass(**i) for i in data]
        data_dict = [asdict(i) for i in obj_data]
        return data_dict

    def is_any_new_data(self, table: str, date: datetime) -> bool:
        """проверяем есть ли более новые записи

        Args:
            table (str): имя таблицы
            date (datetime): время обновления

        Returns:
            bool: True - если новые записи есть.
        """
        qery = self.etl.queries.CHECK_DATA.format(table, date)
        update = self.reader.get_data(qery)
        if update[0]["count"] == 0:
            return False
        return True

    def run(self) -> None:
        """Метод запуска состояния - проверяет все таблицы на
        наличие обновленных записей
        """
        any_new_objects = []

        # Проходим в цикле по всем таблицам
        for table in self.etl.config.TABLES:

            # Получаем соханенную дату обновления по таблице
            time_update = self.get_data_from_storage(
                table=table,
                key="update",
                file_template=self.etl.config.STORING_UPDATE_DATE,
            )
            if time_update:
                time_update = datetime.strptime(
                    time_update["modified"], "%Y-%m-%d %H:%M:%S.%f%z"
                )
            else:
                time_update = datetime.strptime("0", "%S")

            # Проверяем есть ли обновленные записи
            if self.is_any_new_data(table, time_update):
                any_new_objects.append(True)
                # для одной таблицы мб несколько запросов
                # поэтому добавляем цикл
                for data_type in self.etl.config.TABLES[table]:
                    # Если есть получаем пачку записей
                    data = self.etl.postgres.extract_data_from(
                        self.etl.queries.GET_MOVES_FROM[data_type], time_update
                    )
                    data_dict = self.convert_to_dict(
                        data,
                        compare[self.etl.config.TABLES[table][data_type]]["dataclass"],
                    )

                    # обнавляем дату 'modified' для таблицы
                    modified_date = {"modified": data_dict[-1]["modified"]}
                    self.save_data_from_storage(
                        data=modified_date,
                        table=table,
                        key="update",
                        file_template=self.etl.config.STORING_UPDATE_DATE,
                    )

                    # обнавляем временное хранилице новыми данными из базы
                    self.save_data_from_storage(
                        data=data_dict,
                        table=data_type,
                        key=data_type,
                        file_template=self.etl.config.STORING_TABLE_DATA,
                    )
            else:
                any_new_objects.append(False)

        # Если изменения были онаружены запускаем следующие состояния
        if any(any_new_objects):
            log.info("Есть обновления переходим к экспорту изменений.")
            self.etl.state = self.etl.load
            self.etl.run_state()
        # Если изменений ни в одной таблице нет запускам состояние ожидания
        else:
            log.info("Нет обновлений, переходим в режим ожидания.")
            self.etl.state = self.etl.sleep_mode
            self.etl.run_state()


class Load(State):
    """Запись данных в elastic"""

    def __init__(self, etl, elastic: ElasticSearchLoader) -> None:
        """инит метод

        Args:
            etl (main.ETL): Объект управляющего класса состояниями
            elastic (ElasticSearchLoader): Объект класса ElasticSearchLoader
        """
        self.etl = etl
        self.elastic = elastic

    def run(self) -> None:
        """Записывает новые и обновленные записи в индекс"""
        for table in self.etl.config.TABLES:
            # данные из одной таблицы можем заносить в разные циклы
            # реализуем это в цикле
            for data_type in self.etl.config.TABLES[table]:
                # Получаем сохраненные данные из json по каждой таблице
                data_for_load = self.get_data_from_storage(
                    table=data_type,
                    key=data_type,
                    file_template=self.etl.config.STORING_TABLE_DATA,
                )
                # Трансформируем данные в формат индекса
                if not data_for_load:
                    continue
                dict_data = [
                    compare[self.etl.config.TABLES[table][data_type]]["dataclass"](
                        **i
                    ).as_dict()
                    for i in data_for_load
                ]
                # Записываем данные в индекс
                self.elastic.load_data(
                    dict_data=dict_data,
                    index=compare[self.etl.config.TABLES[table][data_type]]["index"],
                )

        log.info("Обновления записаны, переключаемся в состояние Extract.")
        self.etl.state = self.etl.extract
        self.etl.run_state()


class SleepMode(State):
    """Состояние ожидания если обновленных записей нет"""

    def __init__(self, etl) -> None:
        """инит метод

        Args:
            etl (main.ETL): Объект управляющего класса состояниями
        """
        self.etl = etl

    def run(self) -> None:

        sleep(self.etl.config.WAITING_TIME)

        log.info("Время ожидания истекло, переключаемся в состояние Extract.")
        self.etl.state = self.etl.extract
        self.etl.run_state()
