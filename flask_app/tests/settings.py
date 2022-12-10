from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    service_url: str = Field("http://127.0.0.1:5000/api/v1", env="service_url")


test_settings = TestSettings()
