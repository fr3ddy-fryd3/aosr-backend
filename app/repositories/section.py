from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.section import Section
from app.models.section_material import SectionMaterial
from app.schemas.section import SectionSchema, DBSectionSchema


class SectionRepository:
    async def get_all(self, session: AsyncSession) -> list[DBSectionSchema]:
        stmt = select(Section).options(selectinload(Section.materials))
        result = await session.execute(stmt)
        sections = result.scalars().all()

        return [DBSectionSchema.model_validate(db_section) for db_section in sections]

    async def get_by_id(self, session: AsyncSession, id: int) -> DBSectionSchema | None:
        stmt = (
            select(Section)
            .options(selectinload(Section.materials))
            .where(Section.id == id)
        )
        result = await session.execute(stmt)
        section = result.scalars().one_or_none()

        return DBSectionSchema.model_validate(section) if section else None

    async def create(
        self, session: AsyncSession, section_data: SectionSchema
    ) -> DBSectionSchema:
        try:
            section_dict = section_data.model_dump(exclude={"materials"})
            section = Section(**section_dict)

            section.materials = [
                SectionMaterial(**material.model_dump())
                for material in section_data.materials
            ]

            session.add(section)
            await session.commit()
            await session.refresh(section, ["materials"])

            return DBSectionSchema.model_validate(section)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBSectionSchema | None:
        stmt = select(Section).where(Section.id == id)
        result = await session.execute(stmt)
        section = result.scalars().one_or_none()

        if section is None:
            return None

        try:
            columns = [column.name for column in Section.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(section, field, value)
                else:
                    print(f"Поле {field} отсутствует в таблице Material")

            await session.commit()
            return DBSectionSchema.model_validate(section)
        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = (
            select(Section)
            .where(Section.id == id)
            .options(selectinload(Section.materials))
        )
        result = await session.execute(stmt)
        section = result.scalars().one_or_none()

        if section:
            await session.delete(section)
            await session.commit()
            return True
        else:
            return False
