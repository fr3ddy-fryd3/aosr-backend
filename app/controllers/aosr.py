from fastapi import APIRouter

from app.controllers.base import SessionDep
from app.repositories.aosr import AosrRepository
from app.schemas.aosr import AosrSchema, AosrWithMaterialsSchema


aosr_router = APIRouter(prefix="/aosr")


@aosr_router.get("/by_section/")
async def get_aosrs_by_section(session: SessionDep, id: int):
    if id:
        aosrs = await AosrRepository.get_by_section_id(session, id)
        return aosrs
    else:
        return {"message": "Invalid section ID"}


@aosr_router.get("/")
async def get_aosrs(session: SessionDep, id: int = 0):
    if id:
        response = await AosrRepository.get_by_id(session, id)
    else:
        response = await AosrRepository.get_all(session)

    return response


@aosr_router.post("/")
async def create_aosr(session: SessionDep, aosr: AosrWithMaterialsSchema):
    await AosrRepository.create_aosr_and_its_materials(session, aosr)
    return {"message": "Aosr created"}


@aosr_router.post("/several")
async def create_aosrs(session: SessionDep, sections: list[AosrSchema]):
    await AosrRepository.create_many(session, sections)
    return {"message": "Aosrs created"}


@aosr_router.put("/")
async def update_aosr(session: SessionDep, aosr: AosrWithMaterialsSchema):
    await AosrRepository.update_aosr_and_its_materials(session, aosr)
    return {"message": "Aosr updated"}


@aosr_router.delete("/")
async def delete_aosr(session: SessionDep, id: int):
    if id:
        await AosrRepository.delete_by_id(session, id)
        return {"message": "Aosr deleted"}
    else:
        return {"message": "Invalid ID"}
