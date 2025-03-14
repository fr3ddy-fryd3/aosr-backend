from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.passport import Passport
from app.schemas.passport import PassportSchema, DBPassportSchema


class PassportRepository:
    async def get_all(self, session: AsyncSession):
        stmt = select(Passport)
        raw_result = await session.execute(stmt)
        db_passport = raw_result.scalars().all()

        passports = (
            [DBPassportSchema.model_validate(passport) for passport in db_passport]
            if len(db_passport) > 0
            else []
        )

        return passports

    async def get_by_id(self, session: AsyncSession, id: int):
        stmt = select(Passport).where(Passport.id == id)
        raw_result = await session.execute(stmt)
        db_passport = raw_result.scalars().one_or_none()

        passport = DBPassportSchema.model_validate(db_passport) if db_passport else None

        return passport

    async def create(self, session: AsyncSession, passport_data: PassportSchema):
        passport = Passport(**passport_data.model_dump())

        session.add(passport)
        await session.commit()
        await session.refresh(passport)

        return PassportSchema.model_validate(passport)

    async def update(self, session: AsyncSession, id: int, data: dict):
        stmt = select(Passport).where(Passport.id == id)
        raw_result = await session.execute(stmt)
        db_passport = raw_result.scalars().one_or_none()

        if db_passport is None:
            return None

        try:
            columns = [column.name for column in Passport.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(db_passport, field, value)
                else:
                    print(f"Поле {field} отсутствует в таблице Passport")

            await session.commit()
            return DBPassportSchema.model_validate(db_passport)
        except Exception as e:
            print(e)
            await session.rollback()
            return None

    async def delete(self, session: AsyncSession, id: int):
        stmt = select(Passport).where(Passport.id == id)
        raw_result = await session.execute(stmt)
        db_passport = raw_result.scalars().one_or_none()
        if db_passport:
            await session.delete(db_passport)
            await session.commit()
            return DBPassportSchema.model_validate(db_passport)
        else:
            return None
