from sqlalchemy import select, insert

from app.database import async_session_maker


class BaseDAO:
    """
    класс для запросов в бд
    """
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Метод возвращает все записи из таблицы, для git запросов
        """
        async with async_session_maker() as session:    #контекстный менеджер
            # query = select(cls.model).filter_by(**filter_by)    #создание запросаа
            query = select(cls.model.__table__.columns).filter_by(**filter_by)  # создание запросаа # работает
            result = await session.execute(query)    #запрос в бд
            return result.mappings().all()


    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Метод возвращает одну запись из таблицы или None
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)  # создание запросаа
            #query = select(cls.model.__table__.columns).filter_by(**filter_by)  # создание запросаа
            result = await session.execute(query)  # запрос в бд
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        """
        Метод добавляет новую запись в таблицу
        """
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)  # создание запросаа
            await session.execute(query)  # запрос в бд
            await session.commit()  # сохраняем изменения в БД

    @classmethod
    async def find_by_id(cls, model_id: int):
        """
        Метод возвращает запись из таблицы по id
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)  # создание запросаа
            result = await session.execute(query)  # запрос в бд
            return result.scalar_one_or_none()






