from fastapi import APIRouter, Response, status

from app.controllers.base import SessionDep
from app.repositories.aosr import AosrRepository
from app.schemas.aosr import AosrSchema, AosrWithMaterialsSchema


aosr_router = APIRouter(prefix="/aosr")


@aosr_router.get("/by_section/{id}")
async def get_aosrs_by_section(
    session: SessionDep, response: Response, id: int | None = None
):
    if id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Section ID is required"}

    aosrs_response = await AosrRepository.get_by_section_id(session, id)
    return aosrs_response or []


@aosr_router.get("/")
async def get_aosrs(session: SessionDep, response: Response, id: int | None = None):
    if id is not None:
        aosr_response = await AosrRepository.get_by_id(session, id)
        if aosr_response:
            return aosr_response
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "AOSR not found"}
    else:
        aosr_response = await AosrRepository.get_all(session)
        return aosr_response


@aosr_router.post("/")
async def create_aosr(
    session: SessionDep, response: Response, aosr: AosrWithMaterialsSchema
):
    try:
        await AosrRepository.create_aosr_and_its_materials(session, aosr)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "AOSR created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create AOSR: {str(e)}"}


@aosr_router.post("/several")
async def create_aosrs(
    session: SessionDep, response: Response, sections: list[AosrSchema]
):
    try:
        await AosrRepository.create_many(session, sections)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "AOSRs created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create AOSRs: {str(e)}"}


@aosr_router.put("/")
async def update_aosr(
    session: SessionDep, response: Response, aosr: AosrWithMaterialsSchema
):
    try:
        await AosrRepository.update_aosr_and_its_materials(session, aosr)
        response.status_code = status.HTTP_200_OK
        return {"message": "AOSR updated"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to update AOSR: {str(e)}"}


@aosr_router.delete("/{id}")
async def delete_aosr(session: SessionDep, response: Response, id: int):
    try:
        success = await AosrRepository.delete_by_id(session, id)
        if success:
            response.status_code = status.HTTP_200_OK
            return {"message": "AOSR deleted"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "AOSR not found"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to delete AOSR: {str(e)}"}
