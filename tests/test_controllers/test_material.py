import pytest


# Используем TestClient из conftest.py
@pytest.mark.asyncio
async def test_get_empty_materials(test_client):
    response = test_client.get("/material/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_material(test_client):
    material_data = {"name": "Test Material", "units": "kg"}
    response = test_client.post("/material/", json=material_data)
    assert response.status_code == 201
    assert response.json() == {"message": "Material created"}


@pytest.mark.asyncio
async def test_get_materials(test_client):
    response = test_client.get("/material/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_material_by_id(test_client):
    response = test_client.get("/material/?id=1")
    assert response.status_code == 200
    assert "name" in response.json()


@pytest.mark.asyncio
async def test_create_multiple_materials(test_client):
    materials_data = [
        {"name": "Material 1", "units": "m"},
        {"name": "Material 2", "units": "kg"},
    ]
    response = test_client.post("/material/several", json=materials_data)
    assert response.status_code == 201
    assert response.json() == {"message": "Materials created"}


@pytest.mark.asyncio
async def test_update_material(test_client):
    updated_material = {"id": 1, "name": "Updated Material", "units": "liters"}
    response = test_client.put("/material/", json=updated_material)
    assert response.status_code == 200
    assert response.json() == {"message": "Material updated"}


@pytest.mark.asyncio
async def test_delete_material(test_client):
    response = test_client.delete("/material/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Material deleted"}


@pytest.mark.asyncio
async def test_delete_invalid_material(test_client):
    response = test_client.delete("/material/999")
    assert response.status_code == 404
    assert response.json() == {"message": "Material not found"}
