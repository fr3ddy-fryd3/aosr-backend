from fastapi import APIRouter, Response, status

from app.controllers.base import SessionDep
from app.repositories.material import MaterialRepository
from app.schemas.material import MaterialSchema


material_router = APIRouter(prefix="/material")


@material_router.get("/")
async def get_materials(session: SessionDep, response: Response, id: int | None = None):
    if id is not None:
        material_response = await MaterialRepository.get_by_id(session, id)
        if material_response:
            return material_response
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Material not found"}
    else:
        material_response = await MaterialRepository.get_all(session)
        return material_response


@material_router.post("/")
async def create_material(
    session: SessionDep, response: Response, material: MaterialSchema
):
    try:
        await MaterialRepository.create(session, material)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Material created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create material: {str(e)}"}


@material_router.post("/several")
async def create_materials(
    session: SessionDep, response: Response, materials: list[MaterialSchema]
):
    try:
        await MaterialRepository.create_many(session, materials)
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Materials created"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to create materials: {str(e)}"}


@material_router.put("/")
async def update_material(
    session: SessionDep, response: Response, material: MaterialSchema
):
    try:
        await MaterialRepository.update(session, material)
        return {"message": "Material updated"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to update material: {str(e)}"}


@material_router.delete("/")
async def delete_material(session: SessionDep, response: Response, id: int):
    try:
        success = await MaterialRepository.delete_by_id(session, id)
        if success:
            return {"message": "Material deleted"}
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Material not found"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": f"Failed to delete material: {str(e)}"}
