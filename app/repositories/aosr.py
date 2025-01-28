from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.aosr_material import AosrMaterial
from app.repositories.base import BaseRepository
from app.models.aosr import Aosr
from app.schemas.aosr import AosrSchema, AosrWithMaterialsSchema


class AosrRepository(
    BaseRepository[
        Aosr,
        AosrSchema,
    ]
):
    Model = Aosr
    Schema = AosrSchema

    @classmethod
    async def get_by_section_id(
        cls, session: AsyncSession, section_id: int
    ) -> list[Schema]:
        stmt = select(cls.Model).where(cls.Model.section_id == section_id)
        raw_result = await session.scalars(stmt)
        result = raw_result.all()
        aosrs = [cls.Schema.model_validate(aosr) for aosr in result]
        print(aosrs)

        return list(aosrs)

    @classmethod
    async def create_aosr_and_its_materials(
        cls, session: AsyncSession, data: AosrWithMaterialsSchema
    ) -> None:
        aosr = cls.Model(name=data.name, section_id=data.section_id)
        session.add(aosr)
        await session.flush()

        for aosr_material in data.materials:
            aosr_material = AosrMaterial(
                aosr_id=aosr.id,
                material_id=aosr_material.material_id,
                volume=aosr_material.volume,
            )
            session.add(aosr_material)

        await session.commit()

    @classmethod
    async def update_aosr_and_its_materials(
        cls, session: AsyncSession, data: AosrWithMaterialsSchema
    ) -> None:
        aosr = cls.Model(id=data.id, name=data.name, section_id=data.section_id)
        await session.merge(aosr)
        await session.flush()

        for aosr_material in data.materials:
            aosr_material = AosrMaterial(
                id=aosr_material.id,
                aosr_id=aosr.id,
                material_id=aosr_material.material_id,
                volume=aosr_material.volume,
            )
            await session.merge(aosr_material)

        await session.commit()
