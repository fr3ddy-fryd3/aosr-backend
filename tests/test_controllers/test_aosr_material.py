import pytest


@pytest.mark.asyncio
async def test_get_empty_aosr_materials(test_client):
    response = test_client.get("/aosr_material/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_aosr_material(test_client):
    section_data = {
        "name": "Test Section",
        "materials": [{"volume": 10000, "name": "Test Material", "units": "meters"}],
    }
    response = test_client.post("/section/", json=section_data)
    assert response.status_code == 201
    assert response.json() == {"message": "Section created"}

    aosr_data = {
        "name": "Test AOSR",
        "section_id": 1,
        "materials": [],
    }
    response = test_client.post("/aosr/", json=aosr_data)
    assert response.status_code == 201
    assert response.json() == {"message": "AOSR created"}

    aosr_material_data = {"volume": 10000, "aosr_id": 1, "material_id": 1}
    response = test_client.post("/aosr_material/", json=aosr_material_data)
    assert response.status_code == 201
    assert response.json() == {"message": "AOSR material created"}


@pytest.mark.asyncio
async def test_get_aosr_materials(test_client):
    response = test_client.get("/aosr_material/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_aosr_material_by_id(test_client):
    response = test_client.get("/aosr_material/?id=1")
    assert response.status_code == 200
    assert "volume" in response.json()


@pytest.mark.asyncio
async def test_get_aosr_materials_by_aosr_id(test_client):
    response = test_client.get("/aosr_material/by_aosr/1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["aosr_id"] == 1


@pytest.mark.asyncio
async def test_create_multiple_aosr_materials(test_client):
    aosr_materials_data = [
        {"volume": 10000, "aosr_id": 1, "material_id": 1},
        {"volume": 20000, "aosr_id": 1, "material_id": 1},
    ]
    response = test_client.post("/aosr_material/several", json=aosr_materials_data)
    assert response.status_code == 201
    assert response.json() == {"message": "AOSR materials created"}


@pytest.mark.asyncio
async def test_update_aosr_material(test_client):
    aosr_material_data = {"id": 1, "volume": 20000, "aosr_id": 1, "material_id": 1}
    response = test_client.put("/aosr_material/", json=aosr_material_data)
    assert response.status_code == 200
    assert response.json() == {"message": "AOSR material updated"}

    response = test_client.get("/aosr_material/?id=1")
    assert response.status_code == 200
    assert response.json()["volume"] == 20000


@pytest.mark.asyncio
async def test_delete_aosr_material(test_client):
    response = test_client.delete("/aosr_material/1")
    assert response.status_code == 200
    assert response.json() == {"message": "AOSR material deleted"}


@pytest.mark.asyncio
async def test_delete_invalid_aosr_material(test_client):
    response = test_client.delete("/aosr_material/999")
    assert response.status_code == 404
    assert response.json() == {"message": "AOSR material not found"}
