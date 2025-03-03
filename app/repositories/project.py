from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectSchema, DBProjectSchema
from app.schemas.project_material import ProjectMaterialSchema, DBProjectMaterialSchema


class ProjectRepository:
    async def get_all(self, session: AsyncSession):
        stmt = select(Project)
        raw_result = await session.execute(stmt)
        db_projects = raw_result.scalars().all()

        projects = [
            ProjectSchema.model_validate(db_project) for db_project in db_projects
        ]
        return projects

    async def get_by_id(self, session: AsyncSession, id: int):
        stmt = select(Project).where(Project.id == id)
        raw_result = await session.execute(stmt)
        db_project = raw_result.scalars().one_or_none()

        project = ProjectSchema.model_validate(db_project)
        return project

    async def create(self, session: AsyncSession, project: ProjectSchema):
        try:
            pass
        except Exception as e:
            await session.rollback()
            raise e
