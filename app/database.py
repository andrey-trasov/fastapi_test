# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, DeclarativeBase
# from app.config import settings
#
# DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
#
# # создаем движок
# engine = create_async_engine(DATABASE_URL)
#
#
# # создаем гениратор сессий
# async_session_maker = sessionmaker(engine, class_=AsyncSession)
#
# class Base(DeclarativeBase):
#     pass




from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

# создаем движок
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

# создаем генератор сессий
async_session_maker = sessionmaker(engine, class_=AsyncSession)

# создаем базовый класс для моделей
Base = declarative_base()
