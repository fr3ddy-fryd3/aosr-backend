from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.passport import Passport
from app.schemas.passport import PassportSchema, DBPassportSchema


class PassportRepository:
    async def get_all(self, session: AsyncSession) -> list[DBPassportSchema]:
        stmt = select(Passport).options(
            selectinload(Passport.material), selectinload(Passport.aosr_usages)
        )
        result = await session.execute(stmt)
        passports = result.scalars().all()

        return [DBPassportSchema.model_validate(passport) for passport in passports]

    async def get_by_id(
        self, session: AsyncSession, id: int
    ) -> DBPassportSchema | None:
        stmt = select(Passport).where(Passport.id == id)
        result = await session.execute(stmt)
        passport = result.scalars().one_or_none()

        return DBPassportSchema.model_validate(passport) if passport else None

    async def create(
        self, session: AsyncSession, passport_data: PassportSchema
    ) -> DBPassportSchema | None:
        passport = Passport(**passport_data.model_dump())

        session.add(passport)
        await session.commit()
        await session.refresh(passport)

        return DBPassportSchema.model_validate(passport)

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBPassportSchema | None:
        stmt = select(Passport).where(Passport.id == id)
        result = await session.execute(stmt)
        passport = result.scalars().one_or_none()

        if passport is None:
            return None

        try:
            columns = [column.name for column in Passport.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(passport, field, value)
                else:
                    raise ValueError(f"Passport Table hasn't field {field}")

            await session.commit()
            return DBPassportSchema.model_validate(passport)
        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(Passport).where(Passport.id == id)
        result = await session.execute(stmt)
        passport = result.scalars().one_or_none()
        if passport:
            await session.delete(passport)
            await session.commit()
            return True
        else:
            return False
