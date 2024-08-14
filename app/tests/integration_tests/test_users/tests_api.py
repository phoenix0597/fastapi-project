# import asyncio
import pytest

from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("XJqFP@example.com", "test", 200),
    ("XJqFP@example.com", "wrong", 409),
    ("wrong", "test", 422),
])
async def test_register_user(async_client: AsyncClient, email: str, password: str, status_code: int):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    # print(f"{response.status_code=}, {response.text=}, {response.url=}")
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("wrong@person.com", "somepwd", 401),
])
async def test_login_user(async_client: AsyncClient, email: str, password: str, status_code: int):
    response = await async_client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    # print(f"{response.status_code=}, {response.text=}, {response.url=}")
    assert response.status_code == status_code
