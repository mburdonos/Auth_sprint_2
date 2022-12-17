import logging
from http import HTTPStatus
from json import dumps

import backoff
import requests
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis
from requests import post

from api.v1 import films, genres, persons
from core.config import Config, guest, url_compare_permission
from db import elastic, redis

config = Config()

app = FastAPI(
    title="API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1",
    docs_url="/api/v1/movies/openapi",
    openapi_url="/api/v1/movies/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if "/api/v1/movies/openapi" not in request.url.path:
        request_id = {"X-Request-Id": request.headers.get("X-Request-Id")}
        access_token = {
            "access_token_cookie": request.cookies.get("access_token_cookie")
        }
        if access_token.get("access_token_cookie"):
            return_data = post(
                url_compare_permission, cookies=access_token, headers=request_id
            ).json()
            if return_data.get("is_superuser") or return_data.get("roles"):
                response = await call_next(request)
                return response
        if request.url.path in guest:
            response = await call_next(request)
            return response
        return Response(status_code=HTTPStatus.UNAUTHORIZED, content="access is denied")
    response = await call_next(request)
    return response


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


app.include_router(
    films.router, prefix="/api/v1/movies/films", tags=["Поиск по фильмам"]
)
app.include_router(
    genres.router, prefix="/api/v1/movies/genres", tags=["Поиск по жанрам"]
)
app.include_router(
    persons.router, prefix="/api/v1/movies/persons", tags=["Поиск по людям"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000,
    )
