from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.aosr import Aosr
from app.models.aosr_material import AosrMaterial
from app.models.section_material import SectionMaterial
from app.schemas.aosr import AosrSchema, DBAosrSchema, DBAosrSchemaWithoutMaterials


class AosrRepository:
    async def get_all(self, session: AsyncSession) -> list[DBAosrSchema]:
        stmt = select(Aosr).options(
            selectinload(Aosr.materials)
            .selectinload(AosrMaterial.section_material)
            .selectinload(SectionMaterial.material),
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
                selectinload(Aosr.materials)
                .selectinload(AosrMaterial.section_material)
                .selectinload(SectionMaterial.material),
                selectinload(Aosr.materials).selectinload(AosrMaterial.passport_usages),
            )
        )
        result = await session.execute(stmt)
        aosr = result.scalars().one_or_none()

        aosr = DBAosrSchema.model_validate(aosr) if aosr else None
        return aosr

    async def get_by_section(
        self, session: AsyncSession, section_id: int
    ) -> list[DBAosrSchema]:
        stmt = (
            select(Aosr)
            .where(Aosr.section_id == section_id)
            .options(
                selectinload(Aosr.materials)
                .selectinload(AosrMaterial.section_material)
                .selectinload(SectionMaterial.material),
                selectinload(Aosr.materials).selectinload(AosrMaterial.passport_usages),
            )
        )
        result = await session.execute(stmt)
        aosrs = result.scalars().all()

        return [DBAosrSchema.model_validate(aosr) for aosr in aosrs]

    async def create(
        self, session: AsyncSession, aosr_data: AosrSchema
    ) -> DBAosrSchemaWithoutMaterials:
        try:
            aosr_dict = aosr_data.model_dump(exclude={"materials"})
            aosr = Aosr(**aosr_dict)

            session.add(aosr)
            await session.commit()
            await session.refresh(aosr)

            return DBAosrSchemaWithoutMaterials.model_validate(aosr)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBAosrSchemaWithoutMaterials | None:
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
                    raise ValueError(f"Aosr Table hasn't field {field}")

            await session.commit()
            await session.refresh(aosr)

            return DBAosrSchemaWithoutMaterials.model_validate(aosr)
        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(Aosr).where(Aosr.id == id)
        result = await session.execute(stmt)
        aosr = result.scalars().one_or_none()

        if aosr is None:
            return False

        await session.delete(aosr)
        await session.commit()
        return True
