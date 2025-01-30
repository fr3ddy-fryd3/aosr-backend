import pytest


# Используем TestClient из conftest.py
@pytest.mark.asyncio
async def test_get_empty_sections(test_client):
    response = test_client.get("/aosr/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_aosr(test_client):
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
        "materials": [{"volume": 10000, "aosr_id": 1, "material_id": 1}],
    }
    response = response = test_client.post("/aosr/", json=aosr_data)
    assert response.status_code == 201
    assert response.json() == {"message": "AOSR created"}


@pytest.mark.asyncio
async def test_get_aosr(test_client):
    response = test_client.get("/aosr/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_aosr_by_id(test_client):
    response = test_client.get("/aosr/?id=1")
    assert response.status_code == 200
    assert "name" in response.json()


@pytest.mark.asyncio
async def test_create_multiple_aosr(test_client):
    aosrs_data = [
        {
            "name": "Test AOSR 1",
            "section_id": 1,
            "materials": [{"volume": 10000, "aosr_id": 2, "material_id": 1}],
        },
        {
            "name": "Test AOSR 2",
            "section_id": 1,
            "materials": [{"volume": 20000, "aosr_id": 3, "material_id": 1}],
        },
    ]
    response = test_client.post("/aosr/several", json=aosrs_data)
    assert response.status_code == 201
    assert response.json() == {"message": "AOSRs created"}


@pytest.mark.asyncio
async def test_get_aosr_by_section_id(test_client):
    response = test_client.get("/aosr/by_section/?id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_aosr(test_client):
    updated_aosr_data = {
        "id": 1,
        "name": "Test update AOSR",
        "section_id": 1,
        "materials": [{"id": 1, "aosr_id": 1, "material_id": 1, "volume": 20000}],
    }
    response = test_client.put("/aosr/", json=updated_aosr_data)
    assert response.status_code == 200
    assert response.json() == {"message": "AOSR updated"}


@pytest.mark.asyncio
async def test_delete_aosr(test_client):
    response = test_client.delete("/aosr/?id=3")
    assert response.status_code == 200
    assert response.json() == {"message": "AOSR deleted"}


@pytest.mark.asyncio
async def test_delete_invalid_aosr(test_client):
    response = test_client.delete("/aosr/?id=999")
    assert response.status_code == 404
    assert response.json() == {"message": "AOSR not found"}
