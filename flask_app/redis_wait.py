import logging
import time

from redis import Redis

from core.config import configs

if __name__ == "__main__":
    while True:
        try:
            redis_client = Redis(host=configs.redis_host, port=configs.redis_port)
            redis_client.ping()
            break
        except:
            logging.info("Error connect to postgres, sleep 10 sec")
            time.sleep(10)
    redis_client.close()
