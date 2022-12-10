import backoff
import requests
from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
def es_client():
    es_client = Elasticsearch(
        hosts=test_settings.es_host, validate_cert=False, use_ssl=False
    )
    return es_client
