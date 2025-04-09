from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aosr_material import AosrMaterial
from app.schemas.aosr_material import (
    AosrMaterialSchema,
    DBAosrMaterialSchema,
    DBAosrMaterialSchemaForUpdate,
)


class AosrMaterialRepository:
    async def create(
        self, session: AsyncSession, aosr_material_data: AosrMaterialSchema
    ) -> DBAosrMaterialSchema:
        try:
            aosr_material = AosrMaterial(**aosr_material_data.model_dump())

            session.add(aosr_material)
            await session.commit()
            await session.refresh(
                aosr_material, ["section_material", "passport_usages"]
            )
            await session.refresh(aosr_material.section_material, ["material"])

            return DBAosrMaterialSchema.model_validate(aosr_material)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBAosrMaterialSchema | None:
        stmt = select(AosrMaterial).where(AosrMaterial.id == id)
        result = await session.execute(stmt)
        aosr_material = result.scalars().one_or_none()

        if aosr_material is None:
            return None

        if "volume" in data.keys():
            data["volume"] = float(data["volume"])

        try:
            columns = [column.name for column in AosrMaterial.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(aosr_material, field, value)
                else:
                    raise ValueError(f"AosrMaterial Table hasn't field {field}")

            await session.commit()
            await session.refresh(
                aosr_material, ["section_material", "passport_usages"]
            )
            await session.refresh(aosr_material.section_material, ["material"])

            return DBAosrMaterialSchema.model_validate(aosr_material)

        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(AosrMaterial).where(AosrMaterial.id == id)
        result = await session.execute(stmt)
        aosr_material = result.scalars().one_or_none()

        if aosr_material is None:
            return False

        await session.delete(aosr_material)
        await session.commit()
        return True
