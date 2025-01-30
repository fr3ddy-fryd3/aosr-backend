from fastapi import APIRouter, Response, status

from app.controllers.base import SessionDep
from app.repositories.aosr_material import AosrMaterialRepository
from app.schemas.aosr_material import AosrMaterialSchema


aosr_material_router = APIRouter(prefix="/aosr_material")


@aosr_material_router.get("/by_aosr")
async def get_aosr_materials_by_aosr_id(
    session: SessionDep, response: Response, id: int | None = None
):
    if id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "AOSR ID is required"}

    aosr_material_response = await AosrMaterialRepository.get_aosr_materials_by_aosr_id(
        session, id
    )
    return aosr_material_response or []


@aosr_material_router.get("/")
async def get_aosr_materials(
    session: SessionDep, response: Response, id: int | None = None
):
    if id is not None:
        aosr_response = await AosrMaterialRepository.get_by_id(session, id)
        if aosr_response:
            return aosr_response
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "AOSR material not found"}
    else:
        aosr_response = await AosrMaterialRepository.get_all(session)
        return aosr_response


@aosr_material_router.post("/")
async def create_aosr_material(
    session: SessionDep, response: Response, section: AosrMaterialSchema
):
    try:
        await AosrMaterialRepository.create(session, section)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "AOSR material created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create AOSR material: {str(e)}"}


@aosr_material_router.post("/several")
async def create_aosr_materials(
    session: SessionDep, response: Response, sections: list[AosrMaterialSchema]
):
    try:
        await AosrMaterialRepository.create_many(session, sections)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "AOSR materials created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create AOSR materials: {str(e)}"}


@aosr_material_router.put("/")
async def update_aosr_material(
    session: SessionDep, response: Response, section: AosrMaterialSchema
):
    try:
        await AosrMaterialRepository.update(session, section)
        response.status_code = status.HTTP_200_OK
        return {"message": "AOSR material updated"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to update AOSR material: {str(e)}"}


@aosr_material_router.delete("/")
async def delete_aosr_material(session: SessionDep, response: Response, id: int):
    try:
        success = await AosrMaterialRepository.delete_by_id(session, id)
        if success:
            response.status_code = status.HTTP_200_OK
            return {"message": "AOSR material deleted"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "AOSR material not found"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to delete AOSR material: {str(e)}"}
