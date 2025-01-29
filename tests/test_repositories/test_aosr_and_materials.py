import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

# Импорты схем
from app.schemas.aosr import AosrSchema, AosrWithMaterialsSchema
from app.schemas.aosr_material import AosrMaterialSchema
from app.schemas.section import SectionSchema
from app.schemas.material import MaterialSchema

# Импорты репозиториев
from app.repositories.aosr import AosrRepository
from app.repositories.section import SectionRepository
from app.repositories.material import MaterialRepository
from app.repositories.aosr_material import AosrMaterialRepository


# Фикстура для создания тестовой секции
@pytest.fixture
async def create_test_section(session: AsyncSession):
    section = SectionSchema(name="Test section")
    await SectionRepository.create(session, section)
    return section


# Фикстура для создания тестового материала
@pytest.fixture
async def create_test_material(session: AsyncSession):
    material = MaterialSchema(name="Test material", units="kg")
    await MaterialRepository.create(session, material)
    return material


# Фикстура для создания тестового AOSR
@pytest.fixture
async def create_test_aosr(session: AsyncSession, create_test_section):
    aosr = AosrSchema(name="Test aosr", section_id=1)
    await AosrRepository.create(session, aosr)
    return aosr


# Фикстура для создания тестового AOSR с материалами
@pytest.fixture
async def create_test_aosr_with_materials(
    session: AsyncSession, create_test_section, create_test_material
):
    aosr_material = AosrMaterialSchema(aosr_id=1, material_id=1, volume=1)
    aosr_with_materials = AosrWithMaterialsSchema(
        name="Test aosr", section_id=1, materials=[aosr_material]
    )
    await AosrRepository.create_aosr_and_its_materials(session, aosr_with_materials)
    return aosr_with_materials


# Тест получения AOSR по ID секции
@pytest.mark.asyncio
async def test_get_by_section_id(create_test_aosr, session: AsyncSession):
    aosrs = await AosrRepository.get_by_section_id(session, 1)

    assert aosrs is not None
    assert len(aosrs) == 1
    assert aosrs[0].name == "Test aosr"


# Тест создания AOSR с материалами
@pytest.mark.asyncio
async def test_create_aosr_and_its_materials(
    create_test_aosr_with_materials, session: AsyncSession
):
    aosr = await AosrRepository.get_by_id(session, 1)
    assert aosr is not None
    assert aosr.name == "Test aosr"
    assert aosr.section_id == 1


# Тест обновления AOSR и его материалов
@pytest.mark.asyncio
async def test_update_aosr_and_its_materials(
    create_test_aosr_with_materials, session: AsyncSession
):
    # Обновляем AOSR и его материалы
    updated_material = AosrMaterialSchema(id=1, aosr_id=1, material_id=1, volume=2)
    new_material = AosrMaterialSchema(aosr_id=1, material_id=2, volume=3)
    updated_aosr = AosrWithMaterialsSchema(
        id=1,
        name="Updated aosr",
        section_id=2,
        materials=[updated_material, new_material],
    )
    await AosrRepository.update_aosr_and_its_materials(session, updated_aosr)

    # Проверяем обновление AOSR
    aosr = await AosrRepository.get_by_id(session, 1)
    assert aosr is not None
    assert aosr.name == "Updated aosr"
    assert aosr.section_id == 2

    # Проверяем обновление материалов
    materials = await AosrMaterialRepository.get_aosr_materials_by_aosr_id(session, 1)
    assert materials is not None
    assert len(materials) == 2

    # Проверяем первый материал (обновлённый)
    assert materials[0].id == 1
    assert materials[0].volume == 2

    # Проверяем второй материал (новый)
    assert materials[1].material_id == 2
    assert materials[1].volume == 3


# Тест получения материалов по ID AOSR
@pytest.mark.asyncio
async def test_get_aosr_materials_by_aosr_id(
    create_test_aosr_with_materials, session: AsyncSession
):
    # Сценарий 1: Получение материалов для существующего AOSR
    materials = await AosrMaterialRepository.get_aosr_materials_by_aosr_id(session, 1)
    assert materials is not None
    assert len(materials) == 1
    assert materials[0].volume == 1
    assert materials[0].name == "Test material"
    assert materials[0].units == "kg"

    # Сценарий 2: Получение материалов для несуществующего AOSR
    empty_materials = await AosrMaterialRepository.get_aosr_materials_by_aosr_id(
        session, 999
    )
    assert empty_materials == []

    # Сценарий 3: Обработка случая, когда материал отсутствует в таблице Material
    await session.execute(text("DELETE FROM material WHERE id = 1"))
    await session.commit()

    materials_without_material = (
        await AosrMaterialRepository.get_aosr_materials_by_aosr_id(session, 1)
    )
    assert materials_without_material is not None
    assert len(materials_without_material) == 1
    assert materials_without_material[0].name == ""
    assert materials_without_material[0].units == ""
