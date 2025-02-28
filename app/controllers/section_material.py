from fastapi import APIRouter, Response, status

from app.controllers.base import SessionDep
from app.repositories.section_material import SectionMaterialRepository
from app.schemas.section_material import SectionMaterialSchema


section_material_router = APIRouter(prefix="/section_material")


@section_material_router.get("/by_section/{id}")
async def get_section_materials_by_section(
    session: SessionDep, response: Response, id: int | None = None
):
    if id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Section ID is required"}

    section_material_response = await SectionMaterialRepository.get_by_section_id(
        session, id
    )
    return section_material_response or []


@section_material_router.get("/")
async def get_section_material(
    session: SessionDep, response: Response, id: int | None = None
):
    if id is not None:
        section_material_response = await SectionMaterialRepository.get_by_id(
            session, id
        )
        if section_material_response:
            return section_material_response
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Section material not found"}
    else:
        section_material_response = await SectionMaterialRepository.get_all(session)
        return section_material_response


@section_material_router.post("/")
async def create_section_material(
    session: SessionDep, response: Response, section: SectionMaterialSchema
):
    try:
        await SectionMaterialRepository.create(session, section)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Section material created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create section material: {str(e)}"}


@section_material_router.post("/several")
async def create_section_materials(
    session: SessionDep, response: Response, sections: list[SectionMaterialSchema]
):
    try:
        await SectionMaterialRepository.create_many(session, sections)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Section materials created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create section materials: {str(e)}"}


@section_material_router.put("/")
async def update_section_material(
    session: SessionDep, response: Response, section: SectionMaterialSchema
):
    try:
        await SectionMaterialRepository.update(session, section)
        response.status_code = status.HTTP_200_OK
        return {"message": "Section material updated"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to update section material: {str(e)}"}


@section_material_router.delete("/{id}")
async def delete_section_material(session: SessionDep, response: Response, id: int):
    try:
        success = await SectionMaterialRepository.delete_by_id(session, id)
        if success:
            response.status_code = status.HTTP_200_OK
            return {"message": "Section material deleted"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Section material not found"}
    except Exception as e:
        response.status_code = status.HTTP_400
        return {"message": f"Failed to delete section material: {str(e)}"}
