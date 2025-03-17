import logging
from fastapi import APIRouter, Response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .base import SessionDep
from app.repositories.passport import PassportRepository
from app.schemas.passport import PassportSchema

passport_rep = PassportRepository()
passport_router = APIRouter(prefix="/api/v1/passport")


@passport_router.get("/")
async def get_passport(session: SessionDep, response: Response, id: int = 0):
    if id:
        passport_response = await passport_rep.get_by_id(session, id)
        if passport_response:
            return passport_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Passport is not found"}

    else:
        passports_response = await passport_rep.get_all(session)
        return passports_response


@passport_router.post("/")
async def create_passport(
    session: SessionDep, response: Response, passport_data: PassportSchema
):
    try:
        passport_response = await passport_rep.create(session, passport_data)
        response.status_code = HTTP_201_CREATED
        return passport_response
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@passport_router.patch("/{id}")
async def update_passport(
    session: SessionDep, response: Response, id: int, fields: dict
):
    try:
        passport_response = await passport_rep.update(session, id, fields)
        if passport_response:
            return passport_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Passport is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@passport_router.delete("/{id}")
async def delete_passport(session: SessionDep, response: Response, id: int):
    passport_response = await passport_rep.delete(session, id)
    if passport_response:
        response.status_code = HTTP_204_NO_CONTENT
        return passport_response
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Passport is not found"}
