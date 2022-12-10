from http import HTTPStatus
from json import dumps
from typing import List

import pytest

from tests.settings import test_settings


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        # авторизуюсь под пользователем
        (
            {"login": "user1", "password": "pass1"},
            {
                "method": "post",
                "url_api": "/login",
                "status": HTTPStatus.OK,
                "body": {"access_token": "", "refresh_token": ""},
            },
        ),
        # пробую получить данные
        (
            {"login": "", "password": "admin"},
            {
                "method": "get",
                "url_api": "/roles",
                "status": HTTPStatus.OK,
                "body": {"roles": ""},
            },
        ),
        # выхожу из под пользователя
        (
            {"login": "fake_login", "password": ""},
            {
                "method": "get",
                "url_api": "/refresh",
                "status": HTTPStatus.OK,
                "body": {"access_token": "", "refresh_token": ""},
            },
        ),
        # авторизуюсь под админом
        (
            {"login": "", "password": "admin"},
            {
                "method": "get",
                "url_api": "/roles",
                "status": HTTPStatus.OK,
                "body": {"roles": ""},
            },
        ),
        # запрашиваю данные
        (
            {"login": "", "password": "admin"},
            {
                "method": "get",
                "url_api": "/roles",
                "status": HTTPStatus.OK,
                "body": {"roles": ""},
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_login(
    make_get_request,
    make_post_request,
    query_data: List[dict],
    expected_answer: List[dict],
):
    url_api = expected_answer["url_api"]

    if expected_answer["method"] == "get":
        # 3. Запрашиваем данные
        response = await make_get_request(test_settings.service_url + url_api)

    if expected_answer["method"] == "post":
        # 3. Запрашиваем данные
        response = await make_post_request(
            test_settings.service_url + url_api,
            query_data=dumps(query_data),
            cookies=cookies,
        )

    body = await response.json(content_type=None)

    if body.get("access_token"):
        cookies = {"access_token_cookie": body.get("access_token")}

    # заполняем проверяемые поля
    status = response.status
    params = body.keys()

    # 4. Проверяем ответ
    assert status == expected_answer["status"]
    assert params == expected_answer["body"].keys()
