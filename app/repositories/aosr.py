from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.aosr import Aosr
from app.models.aosr_material import AosrMaterial
from app.schemas.aosr import AosrSchema, DBAosrSchema


class AosrRepository:
    async def get_all(self, session: AsyncSession):
        stmt = select(Aosr).options(selectinload(Aosr.materials))
        raw_result = await session.execute(stmt)
        db_aosrs = raw_result.scalars().all()

        aosrs = (
            [DBAosrSchema.model_validate(db_aosr) for db_aosr in db_aosrs]
            if len(db_aosrs) > 0
            else []
        )
        return aosrs

    async def get_by_id(self, session: AsyncSession, id: int):
        stmt = select(Aosr).options(selectinload(Aosr.materials)).where(Aosr.id == id)
        raw_result = await session.execute(stmt)
        db_aosr = raw_result.scalars().one_or_none()

        aosr = DBAosrSchema.model_validate(db_aosr) if db_aosr else None
        return aosr

    async def create(self, session: AsyncSession, aosr_data: AosrSchema):
        try:
            aosr_dict = aosr_data.model_dump(exclude={"materials"})
            aosr = Aosr(**aosr_dict)

            aosr.materials = [
                AosrMaterial(**material.model_dump())
                for material in aosr_data.materials
            ]

            session.add(aosr)
            await session.commit()
            await session.refresh(aosr, ["materials"])

            return DBAosrSchema.model_validate(aosr)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(self, session: AsyncSession, id: int, data: dict):
        stmt = select(Aosr).where(Aosr.id == id)
        raw_result = await session.execute(stmt)
        db_aosr = raw_result.scalars().one_or_none()

        if db_aosr is None:
            return None

        try:
            columns = [column.name for column in Aosr.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(db_aosr, field, value)
                else:
                    print(f"Поле {field} отсутствует в таблице Material")

            await session.commit()
            return DBAosrSchema.model_validate(db_aosr)
        except Exception as e:
            print(e)
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id: int):
        stmt = select(Aosr).where(Aosr.id == id).options(selectinload(Aosr.materials))
        raw_result = await session.execute(stmt)
        db_aosr = raw_result.scalars().one_or_none()

        if db_aosr:
            await session.delete(db_aosr)
            await session.commit()
            return DBAosrSchema.model_validate(db_aosr)
        else:
            return None
