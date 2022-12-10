import sqlite3
import sys
import traceback

import psycopg2
import sql_settings
from postgresql_entry import PostgresSaver
from psycopg2.extensions import connection as _connection
from reading_from_sqlite import SQLiteLoader
from settings import error_log, log
from sql_settings import psql_conn_context, sqlite_conn_context


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, sql_settings.LIMIT)
    sqlite_loader = SQLiteLoader(connection, sql_settings.LIMIT)

    for table in sql_settings.DATABASE_QUERIES:
        data = sqlite_loader.load_data(qeryset=table['read_data'],
                                       dataclass=table['dataclass'])
        for values in data:
            postgres_saver.save_all_data(query=table['save_data'], data=values,
                                         message='пачка записей записана')


if __name__ == '__main__':
    try:
        with sqlite_conn_context(sql_settings.DB_PATH) as sqlite_conn,\
             psql_conn_context(sql_settings.DSL) as pg_conn:
            log.info('Подключение установлено')
            load_from_sqlite(sqlite_conn, pg_conn)

    except (ValueError, StopIteration, sqlite3.Error, psycopg2.Error) as err:
        frame = traceback.extract_tb(sys.exc_info()[2])
        line_no = str(frame[0]).split()[4]
        error_log(line_no)
        log.error(err)
