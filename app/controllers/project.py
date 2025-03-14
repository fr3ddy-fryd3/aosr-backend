from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from .base import SessionDep
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectSchema

project_rep = ProjectRepository()
project_router = APIRouter(prefix="/api/v1/project")


@project_router.get("/")
async def get_project(session: SessionDep, id: int = 0):
    if id:
        project_response = await project_rep.get_by_id(session, id)
        if project_response:
            return project_response
        else:
            raise HTTPException(HTTP_404_NOT_FOUND, "Project is not found")

    else:
        projects_response = await project_rep.get_all(session)
        return projects_response


@project_router.post("/")
async def create_project(
    session: SessionDep, response: Response, project_data: ProjectSchema
):
    project_response = await project_rep.create(session, project_data)
    response.status_code = HTTP_201_CREATED
    return project_response


@project_router.patch("/{id}")
async def update_project(session: SessionDep, id: int, fields: dict):
    project_response = await project_rep.update(session, id, fields)
    if project_response:
        return project_response
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, "project is not found")


@project_router.delete("/{id}")
async def delete_project(session: SessionDep, id: int):
    project_response = await project_rep.delete(session, id)
    if project_response:
        return project_response
    else:
        raise HTTPException(HTTP_404_NOT_FOUND, "Project is not found")
