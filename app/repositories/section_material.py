from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.section_material import SectionMaterial
from app.models.material import Material
from app.schemas.section_material import (
    SectionMaterialSchema,
    SectionMaterialWithNameSchema,
)


class SectionMaterialRepository(BaseRepository[SectionMaterial, SectionMaterialSchema]):
    Model = SectionMaterial
    Schema = SectionMaterialSchema

    @classmethod
    async def get_by_section_id(
        cls, session: AsyncSession, section_id: int
    ) -> list[SectionMaterialWithNameSchema]:
        stmt = (
            select(cls.Model, Material)
            .outerjoin(Material, full=True)
            .where(cls.Model.section_id == section_id)
        )
        print(stmt)
        raw_result = await session.execute(stmt)
        raw_result = raw_result.all()
        result = []

        # данный цикл собирает в один общий объект информацию из
        # двух объектов: Material, SectionMaterial. Это нужно для
        # фронтэнда, для удобной обработки информации
        for pair in raw_result:
            section_material_info = pair[0]
            material_info = pair[1]
            result.append(
                SectionMaterialWithNameSchema(
                    id=section_material_info.id,
                    section_id=section_material_info.section_id,
                    material_id=section_material_info.material_id,
                    name=material_info.name,
                    units=material_info.units,
                    volume=section_material_info.volume,
                )
            )
        return result
