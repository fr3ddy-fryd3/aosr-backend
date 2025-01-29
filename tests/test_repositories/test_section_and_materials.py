import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.section import SectionRepository
from app.repositories.section_material import SectionMaterialRepository
from app.repositories.material import MaterialRepository
from app.schemas.section_material import SectionMaterialWithNameSchema
from app.schemas.section import SectionWithMaterialsSchema


@pytest.fixture
async def create_test_section(session: AsyncSession):
    """
    Фикстура для создания тестовой секции с материалами.
    Возвращает созданную секцию.
    """
    section_material = SectionMaterialWithNameSchema(
        name="Test material", units="kg", volume=1
    )
    section = SectionWithMaterialsSchema(
        name="Test section", materials=[section_material]
    )
    await SectionRepository.create_section_and_its_materials(session, section)
    return section


@pytest.mark.asyncio
async def test_create_section_and_materials(
    clean_db, create_test_section, session: AsyncSession
):
    """
    Тест создания секции с материалами.
    """
    # Получаем раздел, материал и связь между ними
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


@pytest.mark.asyncio
async def test_get_by_section_id(clean_db, create_test_section, session: AsyncSession):
    """
    Тест получения материалов по ID секции.
    """
    section_materials = await SectionMaterialRepository.get_by_section_id(session, 1)

    # Проверяем, что материалы получены
    assert section_materials is not None
    assert len(section_materials) > 0

    # Проверяем поля материала
    assert section_materials[0].units == "kg"
    assert section_materials[0].volume == 1
