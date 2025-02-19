from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# создаем движок
engine = create_async_engine(DATABASE_URL)


# создаем гениратор сессий
async_session_maker = sessionmaker(engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

