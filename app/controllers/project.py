import logging
from fastapi import APIRouter, Response
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .base import SessionDep
from app.repositories.project import ProjectRepository
from app.repositories.project_material import ProjectMaterialRepository
from app.schemas.project import ProjectSchema

project_rep = ProjectRepository()
project_material_rep = ProjectMaterialRepository()
project_router = APIRouter(prefix="/api/v1/project")


@project_router.get("/")
async def get_project(session: SessionDep, response: Response, id: int = 0):
    if id:
        project_response = await project_rep.get_by_id(session, id)
        if project_response:
            return project_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Project is not found"}
    else:
        projects_response = await project_rep.get_all(session)
        return projects_response


@project_router.post("/")
async def create_project(
    session: SessionDep, response: Response, project_data: ProjectSchema
):
    try:
        project_response = await project_rep.create(session, project_data)
        response.status_code = HTTP_201_CREATED
        return project_response
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@project_router.patch("/{id}")
async def update_project(
    session: SessionDep, response: Response, id: int, fields: dict
):
    try:
        project_response = await project_rep.update(session, id, fields)
        if project_response:
            return project_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Project is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@project_router.patch("/material/{id}")
async def update_project_material(
    session: SessionDep, response: Response, id: int, fields: dict
):
    try:
        project_material_response = await project_material_rep.update(
            session, id, fields
        )
        if project_material_response:
            return project_material_response
        else:
            response.status_code = HTTP_404_NOT_FOUND
            return {"msg": "Project material is not found"}
    except Exception as e:
        response.status_code = HTTP_400_BAD_REQUEST
        logging.error(e)
        return {"msg": "Bad request"}


@project_router.delete("/{id}")
async def delete_project(session: SessionDep, response: Response, id: int):
    project_response = await project_rep.delete(session, id)
    if project_response:
        response.status_code = HTTP_204_NO_CONTENT
        return {"msg": "Project is deleted"}
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Project is not found"}


@project_router.delete("/material/{id}")
async def delete_project_material(session: SessionDep, response: Response, id: int):
    project_material_response = await project_material_rep.delete(session, id)
    if project_material_response:
        response.status_code = HTTP_204_NO_CONTENT
        return {"msg": "Project Material is deleted"}
    else:
        response.status_code = HTTP_404_NOT_FOUND
        return {"msg": "Project Material is not found"}
