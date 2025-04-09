from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.passport import PassportUsage
from app.schemas.passport import PassportUsageSchema, DBPassportUsageSchema


class PassportAosrUsageRepository:
    async def get_all(self, session: AsyncSession) -> list[DBPassportUsageSchema]:
        stmt = select(PassportUsage)
        result = await session.execute(stmt)
        passport_usages = result.scalars().all()

        return [
            DBPassportUsageSchema.model_validate(passport_usage)
            for passport_usage in passport_usages
        ]

    async def get_by_id(
        self, session: AsyncSession, id: int
    ) -> DBPassportUsageSchema | None:
        stmt = select(PassportUsage).where(PassportUsage.id == id)
        result = await session.execute(stmt)
        passport_usage = result.scalars().one_or_none()

        return (
            DBPassportUsageSchema.model_validate(passport_usage)
            if passport_usage
            else None
        )

    async def create(
        self, session: AsyncSession, passport_usage_data: PassportUsageSchema
    ) -> DBPassportUsageSchema:
        try:
            passport_usage = PassportUsage(**passport_usage_data.model_dump())

            session.add(passport_usage)
            await session.commit()
            await session.refresh(passport_usage)

            return DBPassportUsageSchema.model_validate(passport_usage)
        except Exception as e:
            await session.rollback()
            raise e

    async def update(
        self, session: AsyncSession, id: int, data: dict
    ) -> DBPassportUsageSchema | None:
        stmt = select(PassportUsage).where(PassportUsage.id == id)
        result = await session.execute(stmt)
        passport_usage = result.scalars().one_or_none()

        if passport_usage is None:
            return None

        try:
            columns = [column.name for column in PassportUsage.__table__.columns]

            for field, value in data.items():
                if field in columns:
                    setattr(passport_usage, field, value)
                else:
                    raise ValueError(f"Passport Usage Table hasn't field {field}")

            await session.commit()
            await session.refresh(passport_usage)

            return DBPassportUsageSchema.model_validate(passport_usage)

        except Exception as e:
            await session.rollback()
            raise e

    async def delete(self, session: AsyncSession, id: int) -> bool:
        stmt = select(PassportUsage).where(PassportUsage.id == id)
        result = await session.execute(stmt)
        passport_usage = result.scalars().one_or_none()

        if passport_usage is None:
            return False

        await session.delete(passport_usage)
        await session.commit()
        return True
