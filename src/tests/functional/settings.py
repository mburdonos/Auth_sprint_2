from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9200", env="elastic_host")
    redis_host: str = Field("127.0.0.1", env="redis_host")
    redis_port: int = Field(6379, env="redis_port")
    service_url: str = Field("http://127.0.0.1:8000", env="service_url")


class FilmTestSettings(TestSettings):
    es_index: str = "movies"
    es_id_field: str = "id"
    api_url: str = "/api/v1/films"


class SearchTestSettings(FilmTestSettings):
    api_url: str = "/api/v1/films/search"


class GenreTestSettings(TestSettings):
    es_index: str = "genre_movies"
    es_id_field: str = "id"
    api_url: str = "/api/v1/genres"


class PersonTestSettings(TestSettings):
    es_index: str = "person_movies"
    es_id_field: str = "id"
    api_url: str = "/api/v1/persons"


test_settings = TestSettings()
film_test_settings = FilmTestSettings()
search_test_settings = SearchTestSettings()
genre_test_settings = GenreTestSettings()
person_test_settings = PersonTestSettings()
