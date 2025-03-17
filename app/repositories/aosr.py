from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.aosr import Aosr
from app.models.aosr_material import AosrMaterial
from app.schemas.aosr import AosrSchema, DBAosrSchema


class AosrRepository:
    async def get_all(self, session: AsyncSession) -> list[DBAosrSchema]:
        stmt = select(Aosr).options(
            selectinload(Aosr.materials).selectinload(AosrMaterial.material),
            selectinload(Aosr.materials).selectinload(AosrMaterial.passport_usages),
        )
        result = await session.execute(stmt)
        aosrs = result.scalars().all()

        return [DBAosrSchema.model_validate(aosr) for aosr in aosrs]

    async def get_by_id(self, session: AsyncSession, id: int) -> DBAosrSchema | None:
        stmt = (
            select(Aosr)
            .where(Aosr.id == id)
            .options(
                selectinload(Aosr.materials).selectinload(AosrMaterial.material),
                selectinload(Aosr.materials).selectinload(AosrMaterial.passport_usages),
            )
        )
        result = await session.execute(stmt)
        aosr = result.scalars().one_or_none()

        aosr = DBAosrSchema.model_validate(aosr) if aosr else None
        return aosr

    async def create(
        self, session: AsyncSession, aosr_data: AosrSchema
    ) -> DBAosrSchema:
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
            for aosr_material in aosr.materials:
                await session.refresh(aosr_material, ["material"])

            return DBAosrSchema.model_validate(aosr)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBAosrSchema | None:
        stmt = select(Aosr).where(Aosr.id == id)
        result = await session.execute(stmt)
        aosr = result.scalars().one_or_none()

        if aosr is None:
            return None

        try:
            columns = [column.name for column in Aosr.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(aosr, field, value)
                else:
                    raise ValueError(f"Поле {field} отсутствует в таблице Material")

            await session.commit()
            await session.refresh(aosr, ["materials"])
            for aosr_material in aosr.materials:
                await session.refresh(aosr_material, ["material"])
                await session.refresh(aosr_material, ["passport_usages"])

            return DBAosrSchema.model_validate(aosr)
        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(Aosr).where(Aosr.id == id).options(selectinload(Aosr.materials))
        result = await session.execute(stmt)
        aosr = result.scalars().one_or_none()

        if aosr:
            await session.delete(aosr)
            await session.commit()
            return True
        else:
            return False
