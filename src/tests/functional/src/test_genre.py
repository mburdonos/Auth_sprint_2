from http import HTTPStatus
from json import dumps, loads
from typing import List

import pytest

from tests.functional.settings import genre_test_settings


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        # Граничные случаи.
        # Вывести все жанры.
        (
            {"filter[name]": "", "page[size]": 100},
            {"status": HTTPStatus.OK, "length": 60},
        ),
        ({"filter[name]": "S"}, {"status": HTTPStatus.OK, "length": 0}),
        (
            {
                "filter[name]": """Markmarkmarkmarkmarkmarkmarkmark
                             markmmarkmarkmarkarkmarkmarkmark
                             markmarkmarkmarkmarkmarkmarkmark
                             markmarkmarkmarkmarkmarkmarkmark
                             markmarkmarkmarkmarkmarkmarkmark
                             markmarkmarkmarkmarkmarkmarkmark
                             markmarkmarkmarkmarkmarkmarkmark"""
            },
            {"status": HTTPStatus.OK, "length": 0},
        ),
        ({"filter[name]": "Star Track"}, {"status": HTTPStatus.OK, "length": 0}),
        # Поиск конкретного жанра.
        ({"filter[name]": "John Johnch1"}, {"status": HTTPStatus.OK, "length": 1}),
        # Поиск этого жанра в Redis
        ({"filter[name]": "John Johnch1"}, {"status": "Redis_data", "length": 1}),
    ],
)
@pytest.mark.asyncio
async def test_search(
    set_data,
    get_data,
    create_key,
    make_get_request,
    es_write_data,
    es_data_genre: List[dict],
    query_data: List[dict],
    expected_answer: List[dict],
):
    # Стираем данные, которые будем сравнивать
    status = None
    length_data = None

    # 2. Загружаем данные в ES
    await es_write_data(
        es_data_genre, genre_test_settings.es_index, genre_test_settings.es_id_field
    )

    # создаём ключ для запроса в redis.
    key = await create_key(query_data, genre_test_settings.api_url)

    # проверяем есть ли данные по ключу  в redis.
    return_data = await get_data(key)

    if not return_data:
        # 3. Запрашиваем данные из ES по API
        response = await make_get_request(
            genre_test_settings.service_url + genre_test_settings.api_url, query_data
        )
        body = await response.json(content_type=None)

        # записываем в redis.
        await set_data(key, dumps(body))

        # заполняем проверяемые поля
        status = response.status
        length_data = len(body)
    else:
        status = "Redis_data"
        length_data = len(loads(return_data))

    # 4. Проверяем ответ
    assert status == expected_answer["status"]
    assert length_data == expected_answer["length"]
