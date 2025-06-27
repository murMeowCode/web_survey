"""Модуль работы с БД"""
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, declared_attr
from main_auth.core.config import Settings

settings = Settings()


class PreBase:
    """предварительная настройка создания таблиц"""

    @declared_attr
    def __tablename__(cls):  # pylint: disable=E0213
        return cls.__name__.lower()  # pylint: disable=E1101

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(Settings().database_url)
async_session_local = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_async_session():
    """генератор асинхронных сессий"""
    async with async_session_local() as async_session:
        yield async_session
