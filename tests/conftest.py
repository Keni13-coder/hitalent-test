import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.base import engine, Base, async_session_maker


@pytest.fixture(scope="module")
def event_loop():
    """Отдельный event loop для pytest-asyncio на всю сессию."""
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()

@pytest.fixture(autouse=True, scope="module")
async def prepare_database():
    """Перед каждым тестом пересоздаём таблицы (чистая БД)."""
    async with engine.begin() as conn:
        
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest.fixture(scope="module")
async def session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
        await session.rollback()