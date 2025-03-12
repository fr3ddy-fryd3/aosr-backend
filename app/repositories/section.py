from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.section import Section
from app.models.section_material import SectionMaterial
from app.schemas.section import SectionSchema, DBSectionSchema


class SectionRepository:
    async def get_all(self, session: AsyncSession):
        stmt = select(Section).options(selectinload(Section.materials))
        raw_result = await session.execute(stmt)
        db_sections = raw_result.scalars().all()

        sections = (
            [DBSectionSchema.model_validate(db_section) for db_section in db_sections]
            if len(db_sections) > 0
            else []
        )
        return sections

    async def get_by_id(self, session: AsyncSession, id: int):
        stmt = (
            select(Section)
            .options(selectinload(Section.materials))
            .where(Section.id == id)
        )
        raw_result = await session.execute(stmt)
        db_section = raw_result.scalars().one_or_none()

        section = DBSectionSchema.model_validate(db_section) if db_section else None
        return section

    async def create(self, session: AsyncSession, section_data: SectionSchema):
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

    async def update(self, session: AsyncSession, id: int, data: dict):
        stmt = select(Section).where(Section.id == id)
        raw_result = await session.execute(stmt)
        db_section = raw_result.scalars().one_or_none()

        if db_section is None:
            return None

        try:
            columns = [column.name for column in Section.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(db_section, field, value)
                else:
                    print(f"Поле {field} отсутствует в таблице Material")

            await session.commit()
            return DBSectionSchema.model_validate(db_section)
        except Exception as e:
            print(e)
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id: int):
        stmt = (
            select(Section)
            .where(Section.id == id)
            .options(selectinload(Section.materials))
        )
        raw_result = await session.execute(stmt)
        db_section = raw_result.scalars().one_or_none()

        if db_section:
            await session.delete(db_section)
            await session.commit()
            return DBSectionSchema.model_validate(db_section)
        else:
            return None
