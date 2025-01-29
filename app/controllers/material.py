from fastapi import APIRouter

from app.controllers.base import SessionDep
from app.repositories.material import MaterialRepository
from app.schemas.material import MaterialSchema


material_router = APIRouter(prefix="/material")


@material_router.get("/")
async def get_materials(session: SessionDep, id: int = 0):
    if id:
        response = await MaterialRepository.get_by_id(session, id)
        return response
    else:
        response = await MaterialRepository.get_all(session)
        return response


@material_router.post("/")
async def create_material(session: SessionDep, material: MaterialSchema):
    await MaterialRepository.create(session, material)
    return {"message": "Material created"}


@material_router.post("/several")
async def create_materials(session: SessionDep, materials: list[MaterialSchema]):
    await MaterialRepository.create_many(session, materials)
    return {"message": "Materials created"}


@material_router.put("/")
async def update_material(session: SessionDep, material: MaterialSchema):
    await MaterialRepository.update(session, material)
    return {"message": "Material updated"}


@material_router.delete("/")
async def delete_material(session: SessionDep, id: int):
    if id is None:
        return {"message": "Invalid ID"}
    elif await MaterialRepository.delete_by_id(session, id):
        return {"message": "Material deleted"}
    else:
        return {"message": "Invalid ID"}
