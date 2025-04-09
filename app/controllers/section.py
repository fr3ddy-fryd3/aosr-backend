import logging
from fastapi import APIRouter, Response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.schemas.section_material import SectionMaterialSchema

from .base import SessionDep
from app.repositories.section import SectionRepository
from app.repositories.section_material import SectionMaterialRepository
from app.schemas.section import SectionSchema

section_rep = SectionRepository()
section_material_rep = SectionMaterialRepository()
section_router = APIRouter(prefix="/api/v1/section")


@section_router.get("/")
async def get_section(session: SessionDep, response: Response, id: int = 0):
    if id:
        section_response = await section_rep.get_by_id(session, id)
        if section_response:
            return section_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Section is not found"}

    else:
        sections_response = await section_rep.get_all(session)
        return sections_response


@section_router.get("/material/{id}")
async def get_section_material_by_id(session: SessionDep, response: Response, id: int):
    section_material_response = await section_material_rep.get_by_id(session, id)
    if section_material_response:
        return section_material_response
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Section Material is not found"}


@section_router.get("/by-project/{project_id}")
async def get_section_by_project(
    session: SessionDep, response: Response, project_id: int
):
    sections_response = await section_rep.get_by_project(session, project_id)
    return sections_response


@section_router.post("/")
async def create_section(
    session: SessionDep, response: Response, section_data: SectionSchema
):
    try:
        section_response = await section_rep.create(session, section_data)
        response.status_code = HTTP_201_CREATED
        return section_response
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@section_router.post("/material")
async def create_section_material(
    session: SessionDep,
    response: Response,
    section_material_data: SectionMaterialSchema,
):
    try:
        section_material_response = await section_material_rep.create(
            session, section_material_data
        )
        response.status_code = HTTP_201_CREATED
        return section_material_response
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@section_router.patch("/{id}")
async def update_section(
    session: SessionDep, response: Response, id: int, fields: dict
):
    try:
        section_response = await section_rep.update(session, id, fields)
        if section_response:
            return section_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Section is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@section_router.patch("/material/{id}")
async def update_section_material(
    session: SessionDep, response: Response, id: int, fields: dict
):
    try:
        section_material_response = await section_material_rep.update(
            session, id, fields
        )
        if section_material_response:
            return section_material_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Section Material is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@section_router.delete("/{id}")
async def delete_section(session: SessionDep, response: Response, id: int):
    section_response = await section_rep.delete(session, id)
    if section_response:
        response.status_code = HTTP_204_NO_CONTENT
        return section_response
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Section is not found"}


@section_router.delete("/material/{id}")
async def delete_section_material(session: SessionDep, response: Response, id: int):
    section_material_response = await section_material_rep.delete(session, id)
    if section_material_response:
        response.status_code = HTTP_204_NO_CONTENT
        return section_material_response
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Section Material is not found"}
