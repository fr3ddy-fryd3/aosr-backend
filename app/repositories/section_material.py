from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.section_material import SectionMaterial
from app.schemas.section_material import DBSectionMaterialSchemaForUpdate


class SectionMaterialRepository:
    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBSectionMaterialSchemaForUpdate | None:
        stmt = select(SectionMaterial).where(SectionMaterial.id == id)
        result = await session.execute(stmt)
        section_material = result.scalars().one_or_none()

        if section_material is None:
            return None

        try:
            columns = [column.name for column in SectionMaterial.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(section_material, field, value)
                else:
                    raise ValueError(f"SectionMaterial Table hasn't field {field}")

            await session.commit()
            await session.refresh(section_material)

            return DBSectionMaterialSchemaForUpdate.model_validate(section_material)

        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(SectionMaterial).where(SectionMaterial.id == id)
        result = await session.execute(stmt)
        section_material = result.scalars().all()

        if section_material is None:
            return False

        await session.delete(section_material)
        await session.commit()
        return True
