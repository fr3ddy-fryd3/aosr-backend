from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

DATABASE_URL = settings.get_db_url()

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL)
# Создаем фабрику сессий для взаимодействия с базой данных
AsyncDBSession = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with AsyncDBSession() as session:
        yield session
