import logging
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.section_material import SectionMaterial
from app.schemas.section_material import (
    DBSectionMaterialSchema,
    DBSectionMaterialSchemaForUpdate,
    SectionMaterialSchema,
)


class SectionMaterialRepository:
    async def get_by_id(
        self, session: AsyncSession, id: int
    ) -> DBSectionMaterialSchema | None:
        try:
            stmt = (
                select(SectionMaterial)
                .where(SectionMaterial.id == id)
                .options(selectinload(SectionMaterial.material))
            )
            result = await session.execute(stmt)
            section_material = result.scalars().one_or_none()

            return DBSectionMaterialSchema.model_validate(section_material)
        except Exception as e:
            logging.error(e)
            return None

    async def create(
        self, session: AsyncSession, section_material_data: SectionMaterialSchema
    ) -> DBSectionMaterialSchema:
        try:
            section_material = SectionMaterial(**section_material_data.model_dump())

            session.add(section_material)
            await session.commit()
            await session.refresh(section_material, ["material"])

            return DBSectionMaterialSchema.model_validate(section_material)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBSectionMaterialSchema | None:
        stmt = select(SectionMaterial).where(SectionMaterial.id == id)
        result = await session.execute(stmt)
        section_material = result.scalars().one_or_none()

        if section_material is None:
            return None

        if "volume" in data.keys():
            data["volume"] = float(data["volume"])

        try:
            columns = [column.name for column in SectionMaterial.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(section_material, field, value)
                else:
                    raise ValueError(f"SectionMaterial Table hasn't field {field}")

            await session.commit()
            await session.refresh(section_material, ["material"])

            return DBSectionMaterialSchema.model_validate(section_material)

        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(SectionMaterial).where(SectionMaterial.id == id)
        result = await session.execute(stmt)
        section_material = result.scalars().one_or_none()

        if section_material is None:
            return False

        await session.delete(section_material)
        await session.commit()
        return True
