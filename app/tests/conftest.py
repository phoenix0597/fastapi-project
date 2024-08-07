import json
from datetime import datetime

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


# @pytest.fixture(scope="session", autouse=True)
@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    print(f"Preparing database... {settings.MODE=}")  # Отладочное сообщение
    if settings.MODE == "TEST":
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                print("Database dropped")
                await conn.run_sync(Base.metadata.create_all)
                print("Database created")
        except Exception as e:
            print(f"Error during database preparation: {e}")


        def open_mock_json(model: str):
            with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
                return json.load(file)

        hotels = open_mock_json("hotels")
        rooms = open_mock_json("rooms")
        users = open_mock_json("users")
        bookings = open_mock_json("bookings")

        for booking in bookings:
            booking["date_from"] = datetime.strftime(booking["date_from"], "%Y-%m-%d")
            booking["date_to"] = datetime.strftime(booking["date_to"], "%Y-%m-%d")

        async with async_session_maker() as session:
            await session.execute(insert(Hotels).values(hotels))
            await session.execute(insert(Rooms).values(rooms))
            await session.execute(insert(Users).values(users))
            await session.execute(insert(Bookings).values(bookings))
            await session.commit()

        yield "Database prepared"

        print("Database prepared.")  # Отладочное сообщение

    else:
        print("Database preparation skipped.")


@pytest.mark.asyncio
async def test_fixture_execution():
    # print(f"{prepare_database=}")
    assert True  # Просто проверяем, что фикстура вызывается