#pylint: disable=W0621
"""Модуль для специтфикации тестовой среды"""
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from main_auth.core.database import Base

@pytest.fixture(scope="session")
async def db_engine():
    """Движок для БД"""
    engine = create_async_engine(os.getenv("DATABASE_URL"))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    """Сессия для БД"""
    async with async_sessionmaker(db_engine, expire_on_commit=False)() as session:
        yield session
        await session.rollback()
