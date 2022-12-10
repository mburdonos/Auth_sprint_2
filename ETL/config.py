import settings
import sql_queries


class Config(object):
    """Класс для хранения настроек проекта"""
    LIMIT = settings.LIMIT
    DSL = settings.DSL
    TABLES = settings.TABLES
    ELASTICSEARCH_URL = settings.ELASTICSEARCH_URL
    INDEX = settings.INDEX
    INDEX_NAME = settings.INDEX_NAME
    STORING_UPDATE_DATE = settings.STORING_UPDATE_DATE
    STORING_TABLE_DATA = settings.STORING_TABLE_DATA
    WAITING_TIME = settings.WAITING_TIME


class Queries(object):
    """Класс для хранения sql-запросов проекта"""
    GET_MOVES_FROM = sql_queries.GET_MOVES_FROM
    GET_MODIFIED_DATE = sql_queries.GET_MODIFIED_DATE
    CHECK_DATA = sql_queries.CHECK_DATA
