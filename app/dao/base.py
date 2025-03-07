from sqlalchemy import insert, select

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
            query = select(cls.model).filter_by(id=model_id)  # создание запроса
            result = await session.execute(query)  # запрос в бд
            return result.scalar_one_or_none()

    @classmethod
    async def update(cls, model_id: int, data):
        """
        Метод изменения запись в таблице
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)  # создание запроса
            result = await session.execute(query)  # запрос в бд
            model_instance = result.scalar_one_or_none()  # получение экземпляра модели
            if model_instance:
                for var, value in vars(data).items():
                    setattr(model_instance, var, value) if value else None
                await session.commit()
            return model_instance

    @classmethod
    async def delete(cls, model_id: int):
        """
        Метод удаления записи из таблицы
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)  # создание запроса
            result = await session.execute(query)
            model_instance = result.scalar_one_or_none()  # получение экземпляра модели
            if model_instance:
                await session.delete(model_instance)
                await session.commit()
            return model_instance
