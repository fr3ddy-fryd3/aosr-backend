from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.project_material import ProjectMaterial
from app.schemas.project import ProjectSchema, DBProjectSchema, DBProjectSchemaForUpdate


class ProjectRepository:
    async def get_all(self, session: AsyncSession) -> list[DBProjectSchema]:
        stmt = select(Project).options(
            selectinload(Project.materials).selectinload(ProjectMaterial.material)
        )
        result = await session.execute(stmt)
        projects = result.scalars().all()

        return [DBProjectSchema.model_validate(project) for project in projects]

    async def get_by_id(self, session: AsyncSession, id: int) -> DBProjectSchema | None:
        # stmt = (
        #     select(Project)
        #     .where(Project.id == id)
        #     .options(
        #         selectinload(Project.materials).selectinload(ProjectMaterial.material)
        #     )
        # )

        stmt = select(Project).where(Project.id == id)
        result = await session.execute(stmt)
        project = result.scalars().one_or_none()

        return DBProjectSchema.model_validate(project) if project else None

    async def create(
        self, session: AsyncSession, project_data: ProjectSchema
    ) -> DBProjectSchema:
        try:
            project_dict = project_data.model_dump(exclude={"materials"})
            project = Project(**project_dict)

            # project.materials = [
            #     ProjectMaterial(**material.model_dump())
            #     for material in project_data.materials
            # ]

            session.add(project)
            await session.commit()
            # await session.refresh(project, ["materials"])
            await session.refresh(project)
            # for project_material in project.materials:
            #     await session.refresh(project_material, ["material"])

            return DBProjectSchema.model_validate(project)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBProjectSchemaForUpdate | None:
        stmt = select(Project).where(Project.id == id)
        result = await session.execute(stmt)
        project = result.scalars().one_or_none()

        if project is None:
            return None

        try:
            columns = [column.name for column in Project.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(project, field, value)
                else:
                    raise ValueError(f"Project Table hasn't field {field}")

            await session.commit()
            await session.refresh(project)

            return DBProjectSchemaForUpdate.model_validate(project)
        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(Project).where(Project.id == id)
        result = await session.execute(stmt)
        project = result.scalars().one_or_none()

        if project is None:
            return False

        await session.delete(project)
        await session.commit()
        return True
