from http import HTTPStatus
from json import dumps
from typing import List

import pytest

from tests.settings import test_settings


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        # передать не существующий логин
        (
            {"login": "fake_login", "password": "admin"},
            {"status": HTTPStatus.UNAUTHORIZED, "body": {"msg": "not valid login"}},
        ),
        # передать не существующий пароль
        (
            {"login": "admin", "password": "fake_password"},
            {"status": HTTPStatus.UNAUTHORIZED, "body": {"msg": "not valid password"}},
        ),
        # передать пустой логин
        (
            {"login": "", "password": "admin"},
            {"status": HTTPStatus.UNAUTHORIZED, "body": {"msg": "not valid login"}},
        ),
        # передать пустой пароль
        (
            {"login": "fake_login", "password": ""},
            {"status": HTTPStatus.UNAUTHORIZED, "body": {"msg": "not valid password"}},
        ),
        # передать корректные данные
        (
            {"login": "admin", "password": "admin"},
            {
                "status": HTTPStatus.OK,
                "body": {"access_token": "", "refresh_token": ""},
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_login(
    make_post_request,
    query_data: List[dict],
    expected_answer: List[dict],
    url_api: str = "/login",
):
    #  Запрашиваем данные
    response = await make_post_request(
        test_settings.service_url + url_api, dumps(query_data)
    )
    body = await response.json(content_type=None)

    # заполняем проверяемые поля
    status = response.status
    params = body.keys()

    # 4. Проверяем ответ
    assert status == expected_answer["status"]
    assert params == expected_answer["body"].keys()
