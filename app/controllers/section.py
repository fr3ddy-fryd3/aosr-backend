from fastapi import APIRouter, Response, status

from app.controllers.base import SessionDep
from app.repositories.section import SectionRepository
from app.schemas.section import SectionSchema, SectionWithMaterialsSchema


section_router = APIRouter(prefix="/section")


@section_router.get("/")
async def get_sections(session: SessionDep, response: Response, id: int | None = None):
    if id is not None:
        section_response = await SectionRepository.get_by_id(session, id)
        if section_response:
            return section_response
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Section not found"}
    else:
        section_response = await SectionRepository.get_all(session)
        return section_response


@section_router.post("/")
async def create_section(
    session: SessionDep, response: Response, data: SectionWithMaterialsSchema
):
    try:
        await SectionRepository.create_section_and_its_materials(session, data)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Section created"}
    except Exception as e:
        return {"message": f"Failed to create section: {str(e)}"}, 400


@section_router.post("/several")
async def create_sections(
    session: SessionDep, response: Response, sections: list[SectionSchema]
):
    try:
        await SectionRepository.create_many(session, sections)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Sections created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create sections: {str(e)}"}


@section_router.put("/")
async def update_section(
    session: SessionDep, response: Response, section: SectionWithMaterialsSchema
):
    try:
        await SectionRepository.update_section_and_its_materials(session, section)
        response.status_code = status.HTTP_200_OK
        return {"message": "Section updated"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to update section: {str(e)}"}


@section_router.delete("/{id}")
async def delete_section(session: SessionDep, response: Response, id: int):
    try:
        success = await SectionRepository.delete_by_id(session, id)
        if success:
            response.status_code = status.HTTP_200_OK
            return {"message": "Section deleted"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Section not found"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to delete section: {str(e)}"}
