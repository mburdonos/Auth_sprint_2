from pydantic import BaseSettings, Field


class Config(BaseSettings):
    project_name: str = Field(env="project_name", default="auth_movies")
    storage_driver: str = Field(env="storage_driver", default="postgresql")
    pg_host: str = Field(env="pg_host", default="127.0.0.1")
    pg_user: str = Field(env="pg_user", default="app")
    pg_password: str = Field(env="pg_password", default="qwe")
    pg_database: str = Field(env="pg_database", default="movies_database")

    redis_host: str = Field(env="redis_host", default="127.0.0.1")
    redis_port: str = Field(env="redis_port", default="6379")

    debug: str = Field(env="debug", default="True") == "True"

    secret_key: str = Field(env="secret_key", default="super-secret")

    yandex_client_id = Field(env="yandex_client_id")
    yandex_client_secret = Field(env="yandex_client_secret")
    yandex_baseurl = Field(env="yandex_baseurl", default=r"https://oauth.yandex.ru/")
    yandex_info_url = Field(env="yandex_baseurl", default=r"https://login.yandex.ru/")

    jaeger_host = Field(env="jaeger_host", default=r"localhost")
    jaeger_port = Field(env="jaeger_port", default=6831)

    class Config:
        env_file = ".env"


configs = Config()
