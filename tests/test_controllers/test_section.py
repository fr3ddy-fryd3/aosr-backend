import pytest


# Используем TestClient из conftest.py
@pytest.mark.asyncio
async def test_get_empty_sections(test_client):
    response = test_client.get("/section/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_section(test_client):
    section_data = {
        "name": "Test Section",
        "materials": [{"volume": 10000, "name": "Test Material", "units": "meters"}],
    }
    response = test_client.post("/section/", json=section_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Section created"}


@pytest.mark.asyncio
async def test_get_section(test_client):
    response = test_client.get("/section/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_section_by_id(test_client):
    response = test_client.get("/section/?id=1")
    assert response.status_code == 200
    assert "name" in response.json()


@pytest.mark.asyncio
async def test_create_multiple_section(test_client):
    sections_data = [
        {
            "name": "Test Section 1",
            "materials": [
                {"volume": 10000, "name": "Test Material", "units": "meters"}
            ],
        },
        {
            "name": "Test Section 2",
            "materials": [
                {"volume": 20000, "name": "Test Material", "units": "meters"}
            ],
        },
    ]
    response = test_client.post("/section/several", json=sections_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Sections created"}


@pytest.mark.asyncio
async def test_update_section(test_client):
    updated_section_data = {
        "id": 1,
        "name": "Test Section",
        "materials": [
            {
                "id": 1,
                "section_id": 1,
                "material_id": 1,
                "volume": 20000,
                "name": "Test Material",
                "units": "meters",
            }
        ],
    }
    response = test_client.put("/section/", json=updated_section_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Section updated"}


@pytest.mark.asyncio
async def test_delete_section(test_client):
    response = test_client.delete("/section/?id=1")
    assert response.status_code == 200
    assert response.json() == {"message": "Section deleted"}


@pytest.mark.asyncio
async def test_delete_invalid_section(test_client):
    response = test_client.delete("/section/?id=999")
    assert response.status_code == 200
    assert response.json() == {"message": "Invalid ID"}
