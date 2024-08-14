# import asyncio
import json
from datetime import datetime, timedelta

import pytest
from sqlalchemy import insert
# from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from app.config import settings
from app.database import Base, async_session_maker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # print(f"\n -Preparing database... {settings.MODE=}")  # Отладочное сообщение
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        # print("Database dropped")
        await conn.run_sync(Base.metadata.create_all)
        # print("Database created")

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    # for booking in bookings:
    #     booking["date_from"] = datetime.strftime(booking["date_from"], "%Y-%m-%d")
    #     booking["date_to"] = datetime.strftime(booking["date_to"], "%Y-%m-%d")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d").date()
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d").date()

    async with async_session_maker() as session:
        await session.execute(insert(Hotels).values(hotels))
        await session.execute(insert(Rooms).values(rooms))
        await session.execute(insert(Users).values(users))
        await session.execute(insert(Bookings).values(bookings))
        await session.commit()

    print("\nDatabase prepared.")  # Отладочное сообщение
    yield "Database prepared"
    # await asyncio.sleep(0)



@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/auth/login", json={"email": "test@test.com", "password": "test",})
        assert ac.cookies["booking_access_token"]
        print(f"{ac.cookies["booking_access_token"]=}")
        yield ac


@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def setup_dates():
    """Фикстура для генерации разных дат"""
    today = datetime.now().date()
    return {
        "today": today,
        "date_soon": today + timedelta(days=1),
        "date_later": today + timedelta(days=31),
        "date_far_later": today + timedelta(days=32),
        "date_before_today": today - timedelta(days=1),
    }
