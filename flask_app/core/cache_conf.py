from flask import Flask
from flask_redis import FlaskRedis

from core.config import configs

cache_client = FlaskRedis()


def cache_init(app: Flask):
    """Инициализация redis"""
    app.config["REDIS_URL"] = f"redis://@{configs.redis_host}:{configs.redis_port}"
    cache_client.init_app(app)
