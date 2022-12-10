from http import HTTPStatus
from json import dumps
from typing import List

import pytest

from tests.settings import test_settings


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        # передать существующий логин
        (
            {
                "login": "admin",
                "password": "admin",
                "email": "maksim@gmail.com",
                "first_name": "Maksim",
                "last_name": "Maksimov",
            },
            {"status": HTTPStatus.UNAUTHORIZED, "body": {"msg": "login exist"}},
        ),
        # передать пустой логин
        (
            {
                "login": "",
                "password": "admin",
                "email": "maksim@gmail.com",
                "first_name": "Maksim",
                "last_name": "Maksimov",
            },
            {
                "status": HTTPStatus.UNAUTHORIZED,
                "body": {"msg": "login or password is empty"},
            },
        ),
        # передать пустой пароль
        (
            {
                "login": "admin",
                "password": "",
                "email": "maksim@gmail.com",
                "first_name": "Maksim",
                "last_name": "Maksimov",
            },
            {
                "status": HTTPStatus.UNAUTHORIZED,
                "body": {"msg": "login or password is empty"},
            },
        ),
        # передать корректные данные
        (
            {
                "login": "user123",
                "password": "password123",
                "email": "maksim@gmail.com",
                "first_name": "Maksim",
                "last_name": "Maksimov",
            },
            {"status": HTTPStatus.OK, "body": {"msg": "create user successful"}},
        ),
    ],
)
@pytest.mark.asyncio
async def test_register(
    make_post_request,
    query_data: List[dict],
    expected_answer: List[dict],
    url_api: str = "/register",
):

    # Запрашиваем данные
    response = await make_post_request(
        test_settings.service_url + url_api, dumps(query_data)
    )
    body = await response.json(content_type=None)

    # заполняем проверяемые поля
    status = response.status
    params = body["msg"]

    # 4. Проверяем ответ
    assert status == expected_answer["status"]
    assert params == expected_answer["body"]["msg"]
