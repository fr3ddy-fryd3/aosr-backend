from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.material import Material
from app.schemas.material import MaterialSchema, DBMaterialSchema


class MaterialRepository:
    async def get_all(self, session: AsyncSession):
        stmt = select(Material)
        raw_result = await session.execute(stmt)
        db_material = raw_result.scalars().all()

        materials = (
            [DBMaterialSchema.model_validate(material) for material in db_material]
            if len(db_material) > 0
            else []
        )

        return materials

    async def get_by_id(self, session: AsyncSession, id: int):
        stmt = select(Material).where(Material.id == id)
        raw_result = await session.execute(stmt)
        db_material = raw_result.scalars().one_or_none()

        material = DBMaterialSchema.model_validate(db_material) if db_material else None

        return material

    async def create(self, session: AsyncSession, material_data: MaterialSchema):
        material = Material(**material_data.model_dump())

        session.add(material)
        await session.commit()
        await session.refresh(material)

        return MaterialSchema.model_validate(material)

    async def update(self, session: AsyncSession, id: int, data: dict):
        stmt = select(Material).where(Material.id == id)
        raw_result = await session.execute(stmt)
        db_material = raw_result.scalars().one_or_none()

        if db_material is None:
            return None

        try:
            columns = [column.name for column in Material.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(db_material, field, value)
                else:
                    print(f"Поле {field} отсутствует в таблице Material")

            await session.commit()
            return DBMaterialSchema.model_validate(db_material)
        except Exception as e:
            print(e)
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id: int):
        stmt = select(Material).where(Material.id == id)
        raw_result = await session.execute(stmt)
        db_material = raw_result.scalars().one_or_none()
        if db_material:
            await session.delete(db_material)
            await session.commit()
            return DBMaterialSchema.model_validate(db_material)
        else:
            return None
