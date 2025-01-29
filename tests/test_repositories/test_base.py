import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.material import Material
from app.schemas.material import MaterialSchema


class TestRepository(BaseRepository[Material, MaterialSchema]):
    Model = Material
    Schema = MaterialSchema


@pytest.mark.asyncio
async def test_create(clean_db, session: AsyncSession):
    material = MaterialSchema(name="Test material", units="kg")

    await TestRepository.create(session, material)

    # Получаем объект по ID, который автоматически присвоится
    row = await TestRepository.get_by_id(session, 1)
    assert row is not None
    assert row.name == "Test material"
    assert row.units == "kg"  # Дополнительная проверка на другие поля


@pytest.mark.asyncio
async def test_get_all(clean_db, session: AsyncSession):
    material_one = MaterialSchema(name="Test material 1", units="kg")
    material_two = MaterialSchema(name="Test material 2", units="kg")

    await TestRepository.create_many(session, [material_one, material_two])

    rows = await TestRepository.get_all(session)
    assert rows is not None
    assert len(rows) == 2
    assert rows[0].name == "Test material 1"
    assert rows[1].name == "Test material 2"

    # Проверка на случай, если в базе нет объектов
    await TestRepository.delete_by_id(session, 1)
    await TestRepository.delete_by_id(session, 2)
    rows_empty = await TestRepository.get_all(session)
    assert len(rows_empty) == 0


@pytest.mark.asyncio
async def test_update(clean_db, session: AsyncSession):
    material = MaterialSchema(name="Test material", units="kg")

    await TestRepository.create(session, material)
    row = await TestRepository.get_by_id(session, 1)
    assert row is not None

    row.name = "Updated material"
    row.units = "lbs"
    await TestRepository.update(session, row)

    # Проверяем все поля
    updated_row = await TestRepository.get_by_id(session, 1)
    assert updated_row is not None
    assert updated_row.name == "Updated material"
    assert updated_row.units == "lbs"


@pytest.mark.asyncio
async def test_delete(clean_db, session: AsyncSession):
    material = MaterialSchema(name="Test material", units="kg")

    await TestRepository.create(session, material)
    await TestRepository.delete_by_id(session, 1)

    # Проверяем, что объект был удалён
    deleted_row = await TestRepository.get_by_id(session, 1)
    assert deleted_row is None


@pytest.mark.asyncio
async def test_get_by_id_not_found(clean_db, session: AsyncSession):
    # Проверка на случай, если объект с таким ID не существует
    result = await TestRepository.get_by_id(session, 999)  # Не существует
    assert result is None
