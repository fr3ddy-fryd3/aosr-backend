from app.models.material import Material
from app.models.section import Section
from app.models.section_material import SectionMaterial
from app.repositories.base import BaseRepository
from app.schemas.section import SectionSchema, SectionWithMaterialsSchema
from sqlalchemy.ext.asyncio import AsyncSession


class SectionRepository(BaseRepository[Section, SectionSchema]):
    Model = Section
    Schema = SectionSchema

    @classmethod
    async def create_section_and_its_materials(
        cls, session: AsyncSession, data: SectionWithMaterialsSchema
    ):
        section = cls.Model(name=data.name)
        session.add(section)
        await session.flush()  # Для получения ID раздела

        for section_material in data.materials:
            if section_material.material_id is not None:
                section_material_entry = SectionMaterial(
                    material_id=section_material.material_id,
                    section_id=section.id,
                    volume=section_material.volume,
                )
                session.add(section_material_entry)
            else:
                new_material = Material(
                    name=section_material.name, units=section_material.units
                )
                session.add(new_material)
                await session.flush()  # Получаем ID нового материала

                section_material_entry = SectionMaterial(
                    material_id=new_material.id,
                    section_id=section.id,
                    volume=section_material.volume,
                )
                session.add(section_material_entry)

        await session.commit()

    @classmethod
    async def update_section_and_its_materials(
        cls, session: AsyncSession, data: SectionWithMaterialsSchema
    ):
        section = cls.Model(id=data.id, name=data.name)
        await session.merge(section)
        await session.flush()  # Получаем актуальную информацию для связки

        for section_material in data.materials:
            if not section_material.material_id:
                new_material = Material(
                    name=section_material.name, units=section_material.units
                )
                session.add(new_material)
                await session.flush()  # Получаем ID нового материала

            material = SectionMaterial(
                id=section_material.id if section_material.id else None,
                section_id=section.id,
                material_id=(
                    new_material.id
                    if "new_material" in locals()
                    else section_material.material_id
                ),
                volume=section_material.volume,
            )

            await session.merge(material)

        await session.commit()

