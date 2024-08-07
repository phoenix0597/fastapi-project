import asyncio

import pytest

from app.config import settings  # для отладочного сообщения
# pytest_plugins = ['pytest_asyncio']


@pytest.mark.asyncio
async def test_abc(prepare_database):
    # print(f"{settings.MODE=}")  # Отладочное сообщение
    # print("\ntest_abc is running...")
    assert 1 == 1


@pytest.mark.asyncio
async def test_fixture_execution(prepare_database):
    # print("\ntest_fixture_execution is running...")
    assert True  # Просто проверяем, что фикстура вызывается


@pytest.mark.asyncio
async def test_async_execution():
    # print("Before sleep")
    await asyncio.sleep(1)
    # print("After sleep")
    assert True
