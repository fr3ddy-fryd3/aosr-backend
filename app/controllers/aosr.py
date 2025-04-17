import logging
from fastapi import APIRouter, Response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.schemas.aosr_material import AosrMaterialSchema

from .base import SessionDep
from app.repositories.aosr import AosrRepository
from app.repositories.aosr_material import AosrMaterialRepository
from app.schemas.aosr import AosrSchema

aosr_rep = AosrRepository()
aosr_material_rep = AosrMaterialRepository()
aosr_router = APIRouter(prefix="/api/v1/aosr")


@aosr_router.get("/")
async def get_aosr(session: SessionDep, response: Response, id: int = 0):
    if id:
        aosr_response = await aosr_rep.get_by_id(session, id)
        if aosr_response:
            return aosr_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Aosr is not found"}

    else:
        aosrs_response = await aosr_rep.get_all(session)
        return aosrs_response


@aosr_router.get("/by-section/{section_id}")
async def get_aosr_by_section(session: SessionDep, response: Response, section_id: int):
    aosrs_response = await aosr_rep.get_by_section(session, section_id)
    return aosrs_response


@aosr_router.get("/by-passport/{passport_id}")
async def get_aosr_by_passport(
    session: SessionDep, response: Response, passport_id: int
):
    aosrs_response = await aosr_rep.get_by_passport(session, passport_id)
    return aosrs_response


@aosr_router.post("/")
async def create_aosr(session: SessionDep, response: Response, aosr_data: AosrSchema):
    try:
        aosr_response = await aosr_rep.create(session, aosr_data)
        response.status_code = HTTP_201_CREATED
        return aosr_response
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@aosr_router.post("/material")
async def create_aosr_material(
    session: SessionDep, response: Response, aosr_material_data: AosrMaterialSchema
):
    try:
        aosr_material_response = await aosr_material_rep.create(
            session, aosr_material_data
        )
        response.status_code = HTTP_201_CREATED
        return aosr_material_response
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@aosr_router.patch("/{id}")
async def update_aosr(session: SessionDep, response: Response, id: int, fields: dict):
    try:
        aosr_response = await aosr_rep.update(session, id, fields)
        if aosr_response:
            return aosr_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Aosr is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@aosr_router.patch("/material/{id}")
async def update_aosr_material(
    session: SessionDep, response: Response, id: int, fields: dict
):
    try:
        aosr_material_response = await aosr_material_rep.update(session, id, fields)
        if aosr_material_response:
            return aosr_material_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Aosr Material is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@aosr_router.delete("/{id}")
async def delete_aosr(session: SessionDep, response: Response, id: int):
    aosr_response = await aosr_rep.delete(session, id)
    if aosr_response:
        response.status_code = HTTP_204_NO_CONTENT
        return aosr_response
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Aosr is not found"}


@aosr_router.delete("/material/{id}")
async def delete_aosr_material(session: SessionDep, response: Response, id: int):
    aosr_material_response = await aosr_material_rep.delete(session, id)
    if aosr_material_response:
        response.status_code = HTTP_204_NO_CONTENT
        return aosr_material_response
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Aosr Material is not found"}
