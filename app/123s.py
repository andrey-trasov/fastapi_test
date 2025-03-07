import asyncio
import json
from datetime import datetime

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import engine, async_session_maker, Base

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users

from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app

# ... (other code)

async def prepare_database():
    # assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests\\mock_{model}.json",  encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_bookings = insert(Bookings).values(bookings)

    await session.execute(add_users)
    await session.execute(add_hotels)
    await session.execute(add_rooms)
    await session.execute(add_bookings)

    await session.commit()

@pytest.fixture(scope="session", autouse=True)
def prepare_database_fixture():
    asyncio.run(prepare_database())

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session

# Call prepare_database coroutine
asyncio.run(prepare_database())