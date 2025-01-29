import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.section import SectionRepository
from app.repositories.section_material import SectionMaterialRepository
from app.repositories.material import MaterialRepository

from app.schemas.section_material import SectionMaterialWithNameSchema
from app.schemas.section import SectionWithMaterialsSchema


@pytest.mark.asyncio
async def test_create_section(session: AsyncSession):
    # Создаем объекты для материалов и секции
    section_material = SectionMaterialWithNameSchema(
        name="Test material", units="kg", volume=1
    )
    section = SectionWithMaterialsSchema(
        name="Test section", materials=[section_material]
    )

    # Создаем секцию с материалами через репозиторий
    await SectionRepository.create_section_and_its_materials(session, section)

    # Получаем раздел и материал по ID
    section_row = await SectionRepository.get_by_id(session, 1)
    material_row = await MaterialRepository.get_by_id(session, 1)
    section_material_row = await SectionMaterialRepository.get_by_id(session, 1)

    # Проверка существования объектов
    assert section_row is not None
    assert material_row is not None
    assert section_material_row is not None

    # Проверка полей
    assert section_row.name == "Test section"
    assert material_row.name == "Test material"
    assert section_material_row.volume == 1
