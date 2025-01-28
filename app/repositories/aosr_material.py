from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.material import Material
from app.repositories.base import BaseRepository
from app.models.aosr_material import AosrMaterial
from app.schemas.aosr_material import AosrMaterialSchema, AosrMaterialWithNameSchema


class AosrMaterialRepository(BaseRepository[AosrMaterial, AosrMaterialSchema]):
    Model = AosrMaterial
    Schema = AosrMaterialSchema

    @classmethod
    async def get_aosr_materials_by_aosr_id(
        cls, session: AsyncSession, aosr_id: int
    ) -> list[AosrMaterialWithNameSchema]:
        stmt = (
            select(cls.Model, Material)
            .outerjoin(Material, full=True)
            .where(cls.Model.aosr_id == aosr_id)
        )
        raw_result = await session.execute(stmt)
        raw_result = raw_result.all()

        # для читаемости следующего блока кода
        aosr_material = 0
        material = 1

        result = [
            AosrMaterialWithNameSchema(
                id=pair[aosr_material].id,
                aosr_id=pair[aosr_material].aosr_id,
                material_id=pair[aosr_material].material_id,
                volume=pair[aosr_material].volume,
                name=pair[material].name if pair[material] else "",
                units=pair[material].units if pair[material] else "",
            )
            for pair in raw_result
        ]

        return result
