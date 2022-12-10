import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Config(BaseSettings):
    """Основные настройки проекта - подключения к другим сервисам и прочее."""

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="movies")

    # Настройки Redis
    REDIS_HOST: str = Field(env="REDIS_HOST", default="127.0.0.1")
    REDIS_PORT: int = Field(env="REDIS_PORT", default=6379)

    # Настройки Elasticsearch
    ELASTIC_HOST: str = Field(env="ELASTIC_HOST", default="127.0.0.1")
    ELASTIC_PORT: int = Field(env="ELASTIC_PORT", default=9200)

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        env_file = ".env"


class Messages(BaseSettings):
    FILM_NOT_FOUND: str = Field(env="FILM_NOT_FOUND", default="not found")
    GENRE_NOT_FOUND: str = Field(env="GENRE_NOT_FOUND", default="not found")
    PERSON_NOT_FOUND: str = Field(env="PERSON_NOT_FOUND", default="not found")

    class Config:
        enf_file = "src/core/messages.txt"
