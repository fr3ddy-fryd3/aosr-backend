from fastapi import APIRouter, Response, status

from app.controllers.base import SessionDep
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectSchema

project_rep = ProjectRepository()
project_router = APIRouter(prefix="/api-v1/project")


@project_router.get("/")
def get_project(session: SessionDep, response: Response, id: int | None):
    if id is not None:
        project_response = project_rep.get_by_id(session, id)
        if project_response:
            return project_response
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
    else:
        project_response = project_rep.get_all(session)
        return project_response


@project_router.post("/")
async def create_project(
    session: SessionDep, response: Response, project_obj: ProjectSchema
):
    pass
