from fastapi import APIRouter

from app.controllers.base import SessionDep
from app.repositories.aosr_material import AosrMaterialRepository
from app.schemas.aosr_material import AosrMaterialSchema


aosr_material_router = APIRouter(prefix="/aosr_material")


@aosr_material_router.get("/by_aosr")
async def get_aosr_materials_by_aosr_id(session: SessionDep, id: int = 0):
    if id:
        response = await AosrMaterialRepository.get_aosr_materials_by_aosr_id(
            session, id
        )
        return response
    else:
        return {"message": "Invalid ID"}


@aosr_material_router.get("/")
async def get_aosr_materials(session: SessionDep, id: int = 0):
    if id:
        response = await AosrMaterialRepository.get_by_id(session, id)
        return response
    else:
        response = await AosrMaterialRepository.get_all(session)
        return response


@aosr_material_router.post("/")
async def create_aosr_material(session: SessionDep, section: AosrMaterialSchema):
    await AosrMaterialRepository.create(session, section)
    return {"message": "Aosr material created"}


@aosr_material_router.post("/several")
async def create_aosr_materials(
    session: SessionDep, sections: list[AosrMaterialSchema]
):
    await AosrMaterialRepository.create_many(session, sections)
    return {"message": "Aosr materials created"}


@aosr_material_router.put("/")
async def update_aosr_material(session: SessionDep, section: AosrMaterialSchema):
    await AosrMaterialRepository.update(session, section)
    return {"message": "Aost material updated"}


@aosr_material_router.delete("/")
async def delete_aosr_material(session: SessionDep, id: int):
    if id:
        await AosrMaterialRepository.delete_by_id(session, id)
        return {"message": "Aosr material deleted"}
    else:
        return {"message": "Invalid ID"}
