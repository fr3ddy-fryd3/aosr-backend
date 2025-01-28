from fastapi import APIRouter

from app.controllers.base import SessionDep
from app.repositories.section import SectionRepository
from app.schemas.section import SectionSchema, SectionWithMaterialsSchema


section_router = APIRouter(prefix="/section")


@section_router.get("/")
async def get_sections(session: SessionDep, id: int = 0):
    if id:
        response = await SectionRepository.get_by_id(session, id)
        return response
    else:
        response = await SectionRepository.get_all(session)
        return response


@section_router.post("/")
async def create_section(session: SessionDep, data: SectionWithMaterialsSchema):
    await SectionRepository.create_section_and_its_materials(session, data)


@section_router.post("/several")
async def create_sections(session: SessionDep, sections: list[SectionSchema]):
    await SectionRepository.create_many(session, sections)
    return {"message": "Sections created"}


@section_router.put("/")
async def update_section(session: SessionDep, section: SectionWithMaterialsSchema):
    await SectionRepository.update_section_and_its_materials(session, section)
    return {"message": "Section updated"}


@section_router.delete("/")
async def delete_section(session: SessionDep, id: int):
    if id:
        await SectionRepository.delete_by_id(session, id)
        return {"message": "Section deleted"}
    else:
        return {"message": "Invalid ID"}
