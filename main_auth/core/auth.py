"""Модуль логики аутентификации"""
from typing import Union
from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy,
)
from sqlalchemy.ext.asyncio import AsyncSession

from main_auth.models.user import User
from main_auth.core.database import get_async_session
from main_auth.schemas.user import UserCreate
from main_auth.core.config import Settings

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Генератор для получения адаптера к БД"""
    yield SQLAlchemyUserDatabase(session,User)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')

def get_jwt_strategy() -> JWTStrategy:
    """Стратегия работы с JWT"""
    return JWTStrategy(secret=Settings().secret,lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Кастомные проверки данных пользователя"""

    async def validate_password(self, password: str,user: Union[UserCreate, User],) -> None:
        """Проверка на длину пароля и дублирование почты в нем
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

async def get_user_manager(user_db=Depends(get_user_db)):
    """Генератор для получения объекта управления пользователями"""
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)