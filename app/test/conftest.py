# import asyncio
# import json
# from datetime import datetime
#
# import pytest
# from sqlalchemy import insert
# from sqlalchemy.ext.declarative import declarative_base
#
# from app.config import settings
# from app.database import engine, async_session_maker
#
# from app.bookings.models import Bookings
# from app.hotels.models import Hotels
# from app.hotels.rooms.models import Rooms
# from app.users.models import Users
#
#
# Base = declarative_base()
#
# @pytest.fixture(scope="session", autouse=True)
# async def prepare_database():
#     assert settings.MODE == "TEST"
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#     def open_mock_json(model: str):
#         with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
#             return json.load(file)
#
#     hotels = open_mock_json("hotels")
#     rooms = open_mock_json("rooms")
#     users = open_mock_json("users")
#     bookings = open_mock_json("bookings")
#
#     for booking in bookings:
#         booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
#         booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")
#
#     async with async_session_maker() as session:
#         add_users = insert(Users).values(users)
#         add_hotels = insert(Hotels).values(hotels)
#         add_rooms = insert(Rooms).values(rooms)
#         add_bookings = insert(Bookings).values(bookings)
#
#     await session.execute(add_users)
#     await session.execute(add_hotels)
#     await session.execute(add_rooms)
#     await session.execute(add_bookings)
#
#     await session.commit()
#
# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

import asyncio
import json
from datetime import datetime
import os

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import async_session_maker  # Убедитесь, что импортируете нужный sessionmaker

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


Base = declarative_base()

# Убедитесь, что MODE установлено в "TEST"
os.environ["MODE"] = "TEST"  # Или используйте другой способ установить переменную окружения
settings.MODE = "TEST"

# Переопределяем engine для тестов
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/test_database"  # Замените на свои параметры
test_engine = create_async_engine(TEST_DATABASE_URL)
TestAsyncSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    print("Preparing database...") # Добавлено для отладки
    assert settings.MODE == "TEST", f"MODE is not TEST, but {settings.MODE}"

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database created")

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with TestAsyncSessionLocal() as session: # Используем тестовую сессию
        add_users = insert(Users).values(users)
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_users)
        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_bookings)

        await session.commit()
    print("Data inserted")

@pytest.fixture(scope="session") #Не используйте эту фикстуру, если вы используете pytest-asyncio
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()