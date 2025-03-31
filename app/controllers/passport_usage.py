import logging
from fastapi import APIRouter, Response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .base import SessionDep
from app.repositories.passport_usages import PassportAosrUsageRepository
from app.schemas.passport import PassportUsageSchema

passport_usage_rep = PassportAosrUsageRepository()
passport_usage_router = APIRouter(prefix="/api/v1/passport-usage")


@passport_usage_router.get("/")
async def get_passport_usage(session: SessionDep, response: Response, id: int = 0):
    if id:
        passport_usage_response = await passport_usage_rep.get_by_id(session, id)
        if passport_usage_response:
            return passport_usage_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Passport Usage is not found"}
    else:
        passport_usage_response = await passport_usage_rep.get_all(session)
        return passport_usage_response


@passport_usage_router.post("/")
async def create_passport_usage(
    session: SessionDep, response: Response, passport_usage_data: PassportUsageSchema
):
    try:
        passport_usage_response = await passport_usage_rep.create(
            session, passport_usage_data
        )
        response.status_code = HTTP_201_CREATED
        return passport_usage_response
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@passport_usage_router.patch("/{id}")
async def update_passport_usage(
    session: SessionDep, response: Response, id: int, fields: dict
):
    try:
        passport_usage_response = await passport_usage_rep.update(session, id, fields)
        if passport_usage_response:
            return passport_usage_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Passport Usage is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@passport_usage_router.delete("/{id}")
async def delete_passport_usage(session: SessionDep, response: Response, id: int):
    passport_usage_response = await passport_usage_rep.delete(session, id)
    if passport_usage_response:
        response.status_code = HTTP_204_NO_CONTENT
        return True
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return False
