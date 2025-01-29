import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient
from database import get_session
from main import app  # импортируй FastAPI приложение из твоего проекта

from app.models.base import Base  # базовый класс моделей

DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # Используем SQLite в памяти для тестов

# Создаём тестовый движок и фабрику сессий
test_engine = create_async_engine(DATABASE_URL, future=True)
TestAsyncDBSession = async_sessionmaker(test_engine, expire_on_commit=False)


# Переопределяем зависимость для получения сессии
async def override_get_session():
    async with TestAsyncDBSession() as session:
        yield session


# Фикстура для тестовой базы данных
@pytest.fixture(scope="module", autouse=True)
async def prepare_test_db():
    # Создаём таблицы перед тестами
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Удаляем таблицы после тестов
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Фикстура для переопределения зависимости FastAPI
@pytest.fixture(scope="module")
def test_client():
    # Подменяем зависимость `get_session` на тестовую
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


# Фикстура для получения сессии в тестах напрямую
@pytest.fixture
async def session():
    async with TestAsyncDBSession() as session:
        yield session
