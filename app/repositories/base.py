from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.base import Base

# Определение обобщенных типов
M = TypeVar("M", bound=Base)
S = TypeVar("S", bound=BaseModel)


# Базовый репозиторий для работы с моделями базы данных
class BaseRepository[M, S]:
    Model: type[M]
    Schema: type[S]

    @classmethod
    async def _execute_commit(cls, session: AsyncSession):
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    # Получение объекта по ID
    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> S | None:
        stmt = select(cls.Model).where(cls.Model.id == id)
        raw_result = await session.scalars(stmt)
        raw_result = raw_result.one_or_none()
        if raw_result is not None:
            result = cls.Schema.model_validate(raw_result)
            return result
        else:
            return None

    # Получение всех объектов
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[S]:
        stmt = select(cls.Model)
        raw_result = await session.scalars(stmt)
        result = [cls.Schema.model_validate(obj) for obj in raw_result.all()]
        return result

    # Создание нового объекта
    @classmethod
    async def create(cls, session: AsyncSession, obj: S) -> None:
        new_obj = cls.Model(**obj.model_dump())
        print(new_obj)
        session.add(new_obj)
        await cls._execute_commit(session)

    # Создание нескольких новых объектов
    @classmethod
    async def create_many(cls, session: AsyncSession, objs: list[S]) -> None:
        new_objs = [cls.Model(**obj.model_dump()) for obj in objs]
        session.add_all(new_objs)
        await cls._execute_commit(session)

    # Обновление существующего объекта
    @classmethod
    async def update(cls, session: AsyncSession, obj: S) -> None:
        await session.merge(cls.Model(**obj.model_dump()))
        await cls._execute_commit(session)

    # Удаление объекта по ID
    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id: int) -> None:
        stmt = select(cls.Model).where(cls.Model.id == id)
        obj = await session.scalars(stmt)
        await session.delete(obj.one_or_none())
        await cls._execute_commit(session)
