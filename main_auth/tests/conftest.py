# pylint: disable=W0621
"""Модуль для спецификации тестовой среды"""
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from main_auth.core.database import Base

@pytest.fixture(scope="session", autouse=True)
async def db_engine():
    """Движок для БД с автоматическим созданием/удалением таблиц"""
    engine = create_async_engine(
        os.getenv("DATABASE_URL"),
        echo=True  # Включаем логирование SQL-запросов для отладки
    )

    # Явно создаем все таблицы
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Очищаем БД после тестов
    async with engine.begin() as conn:
        print("Dropping tables...")
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    """Сессия для БД с автоматическим откатом изменений"""
    async with async_sessionmaker(
        db_engine,
        expire_on_commit=False,
        autoflush=False
    )() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
