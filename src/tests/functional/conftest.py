import asyncio

import pytest

pytest_plugins = [
    "tests.functional.fixtures.conf_elastic",
    "tests.functional.fixtures.conf_redis",
    "tests.functional.fixtures.conf_gendata",
    "tests.functional.fixtures.conf_http",
]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
