"""Модель пользователя"""
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from main_auth.core.database import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    """Инициализация модели пользователя"""
