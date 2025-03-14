from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from .base import SessionDep
from app.repositories.passport import PassportRepository
from app.schemas.passport import PassportSchema

passport_rep = PassportRepository()
passport_router = APIRouter(prefix="/api/v1/passport")


@passport_router.get("/")
async def get_passport(session: SessionDep, id: int = 0):
    if id:
        passport_response = await passport_rep.get_by_id(session, id)
        if passport_response:
            return passport_response
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, "Passport is not found")

    else:
        passports_response = await passport_rep.get_all(session)
        return passports_response


@passport_router.post("/")
async def create_passport(
    session: SessionDep, response: Response, passport_data: PassportSchema
):
    passport_response = await passport_rep.create(session, passport_data)
    response.status_code = HTTP_201_CREATED
    return passport_response


@passport_router.patch("/{id}")
async def update_passport(session: SessionDep, id: int, fields: dict):
    passport_response = await passport_rep.update(session, id, fields)
    if passport_response:
        return passport_response
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, "Passport is not found")


@passport_router.delete("/{id}")
async def delete_passport(session: SessionDep, id: int):
    passport_response = await passport_rep.delete(session, id)
    if passport_response:
        return passport_response
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, "Passport is not found")
