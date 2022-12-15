import logging
import time

import psycopg2

from core.config import configs


if __name__ == "__main__":
    time.sleep(90)
    while True:
        try:
            connection = psycopg2.connect(
                user=configs.pg_user,
                password=configs.pg_password,
                host=configs.pg_host,
                database=configs.pg_database,
            )
            break
        except:
            logging.info("Error connect to postgres, sleep 10 sec")
            time.sleep(10)
    connection.close()
