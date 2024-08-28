from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.logger import logger


class BaseDAO:
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def add_bulk(cls, *data):
        try:
            # Преобразуем кортеж данных в список словарей
            formatted_data = list(data[0])

            # Вставляем данные в таблицу
            query = insert(cls.model).values(formatted_data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            msg = "Database Exc" if isinstance(e, SQLAlchemyError) else "Unknown Exc"
            msg += ": Cannot bulk insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None