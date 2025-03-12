from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from .base import SessionDep
from app.repositories.section import SectionRepository
from app.schemas.section import SectionSchema

section_rep = SectionRepository()
section_router = APIRouter(prefix="/api/v1/section")


@section_router.get("/")
async def get_section(session: SessionDep, id: int = 0):
    if id:
        section_response = await section_rep.get_by_id(session, id)
        if section_response:
            return section_response
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, "Section is not found")

    else:
        sections_response = await section_rep.get_all(session)
        return sections_response


@section_router.post("/")
async def create_section(
    session: SessionDep, response: Response, section_data: SectionSchema
):
    section_response = await section_rep.create(session, section_data)
    response.status_code = HTTP_201_CREATED
    return section_response


@section_router.delete("/{id}")
async def delete_section(session: SessionDep, id: int):
    section_response = await section_rep.delete(session, id)
    if section_response:
        return section_response
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, "Section is not found")
