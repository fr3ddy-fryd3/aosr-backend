from fastapi import responses
import pytest
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.section import SectionSchema
from app.schemas.material import MaterialSchema
from app.repositories.section import SectionRepository
from app.repositories.material import MaterialRepository


# Используем TestClient из conftest.py
@pytest.mark.asyncio
async def test_prepare_section_and_material(test_client):
    response = test_client.post(
        "/section/", json={"name": "Test section 1", "materials": []}
    )
    assert response.status_code == 201
    response = test_client.post(
        "/section/", json={"name": "Test section 2", "materials": []}
    )
    assert response.status_code == 201

    response = test_client.post(
        "/material/", json={"name": "Test material 1", "units": "kg"}
    )
    assert response.status_code == 201
    response = test_client.post(
        "/material/", json={"name": "Test material 2", "units": "kg"}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_empty_section_materials(test_client):
    """
    Тест получения пустого списка материалов секций.
    """
    response = test_client.get("/section_material/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_section_material(test_client):
    """
    Тест создания материала секции.
    """
    section_material_data = {
        "section_id": 1,
        "material_id": 1,
        "volume": 10000,
    }
    response = test_client.post("/section_material/", json=section_material_data)
    assert response.status_code == 201
    assert response.json() == {"message": "Section material created"}


@pytest.mark.asyncio
async def test_create_multiple_section_materials(test_client):
    """
    Тест создания нескольких материалов секций.
    """
    section_materials_data = [
        {"section_id": 1, "material_id": 1, "volume": 10000},
        {"section_id": 2, "material_id": 2, "volume": 20000},
    ]
    response = test_client.post(
        "/section_material/several", json=section_materials_data
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Section materials created"}


@pytest.mark.asyncio
async def test_get_section_material_by_id(test_client):
    """
    Тест получения материала секции по ID.
    """
    # Затем получаем его по ID
    response = test_client.get("/section_material/?section_material_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["section_id"] == 1
    assert data["material_id"] == 1
    assert data["volume"] == 10000


@pytest.mark.asyncio
async def test_get_section_materials_by_section(test_client):
    """
    Тест получения материалов секции по ID секции.
    """
    response = test_client.get("/material/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Получаем материалы по ID секции
    response = test_client.get("/section_material/by_section/?id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["section_id"] == 1
    assert data[1]["section_id"] == 1


@pytest.mark.asyncio
async def test_update_section_material(test_client):
    """
    Тест обновления материала секции.
    """
    # Сначала создаём материал
    section_material_data = {
        "section_id": 1,
        "material_id": 1,
        "volume": 10000,
    }
    create_response = test_client.post("/section_material/", json=section_material_data)
    assert create_response.status_code == 201

    # Затем обновляем его
    updated_data = {
        "id": 1,
        "section_id": 1,
        "material_id": 1,
        "volume": 20000,
    }
    update_response = test_client.put("/section_material/", json=updated_data)
    assert update_response.status_code == 200
    assert update_response.json() == {"message": "Section material updated"}

    # Проверяем, что материал обновился
    get_response = test_client.get("/section_material/?section_material_id=1")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["volume"] == 20000


@pytest.mark.asyncio
async def test_delete_section_material(test_client):
    """
    Тест удаления материала секции.
    """
    # Сначала создаём материал
    section_material_data = {
        "section_id": 1,
        "material_id": 1,
        "volume": 10000,
    }
    create_response = test_client.post("/section_material/", json=section_material_data)
    assert create_response.status_code == 201

    # Затем удаляем его
    delete_response = test_client.delete("/section_material/?id=1")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Section material deleted"}

    # Проверяем, что материал удалён
    get_response = test_client.get("/section_material/?section_material_id=1")
    assert get_response.status_code == 404
    assert get_response.json() == {"message": "Section material not found"}


@pytest.mark.asyncio
async def test_delete_invalid_section_material(test_client):
    """
    Тест удаления несуществующего материала секции.
    """
    response = test_client.delete("/section_material/?id=999")
    assert response.json() == {"message": "Section material not found"}
