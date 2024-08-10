import asyncio
import json
from datetime import datetime

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

    yield "Database prepared"
    await asyncio.sleep(0)

    print("\nDatabase prepared.")  # Отладочное сообщение


@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# пример использование в тесте предыдущей фикстуры
# async def test_abc(ac):
#     await ac.get("/")