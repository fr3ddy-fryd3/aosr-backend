import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.section import SectionRepository
from app.repositories.section_material import SectionMaterialRepository

from app.schemas.section_material import SectionMaterialWithNameSchema
from app.schemas.section import SectionWithMaterialsSchema


@pytest.mark.asyncio
async def test_get_by_section_id(session: AsyncSession):
    # Создаем объекты для материалов и секции
    section_material = SectionMaterialWithNameSchema(
        name="Test material", units="kg", volume=1
    )
    section = SectionWithMaterialsSchema(
        name="Test section", materials=[section_material]
    )

    # Создаем секцию с материалами через репозиторий
    await SectionRepository.create_section_and_its_materials(session, section)

    sections = await SectionMaterialRepository.get_by_section_id(session, 1)
    assert sections is not None
    assert sections[0].units == "kg"
    assert sections[0].volume == 1
