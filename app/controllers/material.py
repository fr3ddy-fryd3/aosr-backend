from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from .base import SessionDep
from app.repositories.material import MaterialRepository
from app.schemas.material import MaterialSchema

material_rep = MaterialRepository()
material_router = APIRouter(prefix="/api/v1/material")


@material_router.get("/")
async def get_material(session: SessionDep, id: int = 0):
    if id:
        material_response = await material_rep.get_by_id(session, id)
        if material_response:
            return material_response
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, "Material is not found")

    else:
        materials_response = await material_rep.get_all(session)
        return materials_response


@material_router.post("/")
async def create_material(
    session: SessionDep, response: Response, material_data: MaterialSchema
):
    material_response = await material_rep.create(session, material_data)
    response.status_code = HTTP_201_CREATED
    return material_response


@material_router.patch("/{id}")
async def update_material(session: SessionDep, id: int, fields: dict):
    material_response = await material_rep.update(session, id, fields)
    if material_response:
        return material_response
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, "Material is not found")


@material_router.delete("/{id}")
async def delete_material(session: SessionDep, id: int):
    material_response = await material_rep.delete(session, id)
    if material_response:
        return material_response
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, "Material is not found")
