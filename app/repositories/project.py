from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.project_material import ProjectMaterial
from app.schemas.project import ProjectSchema, DBProjectSchema


class ProjectRepository:
    async def get_all(self, session: AsyncSession):
        stmt = select(Project).options(selectinload(Project.materials))
        raw_result = await session.execute(stmt)
        db_projects = raw_result.scalars().all()

        projects = (
            [DBProjectSchema.model_validate(db_project) for db_project in db_projects]
            if len(db_projects) > 0
            else []
        )
        return projects

    async def get_by_id(self, session: AsyncSession, id: int):
        stmt = (
            select(Project)
            .where(Project.id == id)
            .options(selectinload(Project.materials))
        )
        raw_result = await session.execute(stmt)
        db_project = raw_result.scalars().one_or_none()

        project = DBProjectSchema.model_validate(db_project) if db_project else None
        return project

    async def create(self, session: AsyncSession, project_data: ProjectSchema):
        try:
            project_dict = project_data.model_dump(exclude={"materials"})
            project = Project(**project_dict)

            project.materials = [
                ProjectMaterial(**material.model_dump())
                for material in project_data.materials
            ]

            session.add(project)
            await session.commit()
            await session.refresh(project, ["materials"])

            return DBProjectSchema.model_validate(project)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(self, session: AsyncSession, id: int, data: dict):
        stmt = select(Project).where(Project.id == id)
        raw_result = await session.execute(stmt)
        db_project = raw_result.scalars().one_or_none()

        if db_project is None:
            return None

        try:
            columns = [column.name for column in Project.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(db_project, field, value)
                else:
                    print(f"Поле {field} отсутствует в таблице Material")

            await session.commit()
            return DBProjectSchema.model_validate(db_project)
        except Exception as e:
            print(e)
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id: int):
        stmt = (
            select(Project)
            .where(Project.id == id)
            .options(selectinload(Project.materials))
        )
        raw_result = await session.execute(stmt)
        db_project = raw_result.scalars().one_or_none()

        if db_project:
            await session.delete(db_project)
            await session.commit()
            return DBProjectSchema.model_validate(db_project)
        else:
            return None
