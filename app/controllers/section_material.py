from fastapi import APIRouter

from app.controllers.base import SessionDep
from app.repositories.section_material import SectionMaterialRepository
from app.schemas.section_material import SectionMaterialSchema


section_material_router = APIRouter(prefix="/section_material")


@section_material_router.get("/by_section/")
async def get_section_materials_by_section(session: SessionDep, id: int = 0):
    if id:
        response = await SectionMaterialRepository.get_by_section_id(session, id)
        return response
    else:
        return {"message": "Invalid section ID"}


@section_material_router.get("/")
async def get_section_material(session: SessionDep, section_material_id: int):
    if section_material_id:
        response = await SectionMaterialRepository.get_by_id(
            session, section_material_id
        )
        return response
    else:
        response = await SectionMaterialRepository.get_all(session)
        return response


@section_material_router.post("/")
async def create_section_material(session: SessionDep, section: SectionMaterialSchema):
    await SectionMaterialRepository.create(session, section)

    return {"message": "Section material created"}


@section_material_router.post("/several")
async def create_section_materials(
    session: SessionDep, sections: list[SectionMaterialSchema]
):
    await SectionMaterialRepository.create_many(session, sections)
    return {"message": "Section materials created"}


@section_material_router.put("/")
async def update_section_material(session: SessionDep, section: SectionMaterialSchema):
    await SectionMaterialRepository.update(session, section)
    return {"message": "Section material updated"}


@section_material_router.delete("/")
async def delete_section_material(session: SessionDep, id: int):
    if id:
        await SectionMaterialRepository.delete_by_id(session, id)
        return {"message": "Section material deleted"}
    else:
        return {"message": "Invalid section material ID"}
