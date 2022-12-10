from pydantic import BaseSettings, Field


class Config(BaseSettings):
    storage_driver: str = Field(env="storage_driver", default="postgresql")
    pg_host: str = Field(env="pg_host", default="127.0.0.1")
    pg_user: str = Field(env="pg_user", default="app")
    pg_password: str = Field(env="pg_password", default="qwe")
    pg_database: str = Field(env="pg_database", default="movies_database")

    redis_host: str = Field(env="redis_host", default="127.0.0.1")
    redis_port: str = Field(env="redis_port", default="6379")

    debug: str = Field(env="debug", default="True") == "True"

    secret_key: str = Field(env="secret_key", default="super-secret")

    class Config:
        env_file = ".env"


configs = Config()
