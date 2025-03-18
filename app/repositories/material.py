from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.material import Material
from app.schemas.material import MaterialSchema, DBMaterialSchema


class MaterialRepository:
    async def get_all(self, session: AsyncSession) -> list[DBMaterialSchema]:
        stmt = select(Material)
        result = await session.execute(stmt)
        materials = result.scalars().all()

        return [DBMaterialSchema.model_validate(material) for material in materials]

    async def get_by_id(
        self, session: AsyncSession, id: int
    ) -> DBMaterialSchema | None:
        stmt = select(Material).where(Material.id == id)
        result = await session.execute(stmt)
        material = result.scalars().one_or_none()

        return DBMaterialSchema.model_validate(material) if material else None

    async def create(
        self, session: AsyncSession, material_data: MaterialSchema
    ) -> DBMaterialSchema:
        try:
            material = Material(**material_data.model_dump())

            session.add(material)
            await session.commit()
            await session.refresh(material)

            return DBMaterialSchema.model_validate(material)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBMaterialSchema | None:
        stmt = select(Material).where(Material.id == id)
        result = await session.execute(stmt)
        material = result.scalars().one_or_none()

        if material is None:
            return None

        try:
            columns = [column.name for column in Material.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(material, field, value)
                else:
                    raise ValueError(f"Material Table hasn't field {field}")

            await session.commit()
            return DBMaterialSchema.model_validate(material)
        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(Material).where(Material.id == id)
        raw_result = await session.execute(stmt)
        db_material = raw_result.scalars().one_or_none()
        if db_material:
            await session.delete(db_material)
            await session.commit()
            return True
        else:
            return False
