from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_material import ProjectMaterial
from app.schemas.project_material import (
    DBProjectMaterialSchema,
    ProjectMaterialSchema,
    DBProjectMaterialSchemaForUpdate,
)


class ProjectMaterialRepository:
    async def create(
        self, session: AsyncSession, project_material_data: ProjectMaterialSchema
    ) -> DBProjectMaterialSchema:
        try:
            project_material = ProjectMaterial(**project_material_data.model_dump())

            session.add(project_material)
            await session.commit()
            await session.refresh(project_material, ["material"])
            print(project_material.volume, project_material.id)

            return DBProjectMaterialSchema.model_validate(project_material)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBProjectMaterialSchemaForUpdate | None:
        stmt = select(ProjectMaterial).where(ProjectMaterial.id == id)
        result = await session.execute(stmt)
        project_material = result.scalars().one_or_none()

        if project_material is None:
            return None

        try:
            columns = [column.name for column in ProjectMaterial.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(project_material, field, value)
                else:
                    raise ValueError(f"ProjectMaterial Table hasn't field {field}")

            await session.commit()
            await session.refresh(project_material, ["material"])

            return DBProjectMaterialSchemaForUpdate.model_validate(project_material)

        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(ProjectMaterial).where(ProjectMaterial.id == id)
        result = await session.execute(stmt)
        project_material = result.scalars().one_or_none()

        if project_material is None:
            return False

        await session.delete(project_material)
        await session.commit()
        return True
