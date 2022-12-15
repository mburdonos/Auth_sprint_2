import logging

import backoff
import requests
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis

from api.v1 import films, genres, persons
from core.config import Config
from db import elastic, redis

config = Config()

app = FastAPI(
    title="API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
@app.on_event("startup")
async def startup():
    redis.redis_conn = await aioredis.Redis(
        host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True
    )
    logging.info("initialized redis connection.")
    elastic.es_conn = AsyncElasticsearch(
        hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"]
    )
    logging.info("initialized elasticsearch connection.")


@app.on_event("shutdown")
async def shutdown():
    if redis.redis_conn is not None:
        redis.redis_conn.close()
        await redis.redis_conn.wait_closed()
        logging.info("closed redis connection.")
    if elastic.es_conn is not None:
        await elastic.es_conn.close()
        logging.info("closed elasticsearch connection.")


app.include_router(films.router, prefix="/api/v1/movies/films", tags=["Поиск по фильмам"])
app.include_router(genres.router, prefix="/api/v1/movies/genres", tags=["Поиск по жанрам"])
app.include_router(persons.router, prefix="/api/v1/movies/persons", tags=["Поиск по людям"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000,
    )
