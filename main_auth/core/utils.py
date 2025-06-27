"""вспомогательные функции"""
from fastapi import Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.core.database import get_async_session
from main_auth.core.jwt_logic import verify_password
from main_auth.models.user import User

async def get_user_by_id(user_id : int, session : AsyncSession = Depends(get_async_session)):
    """Получение пользователя из БД по его id"""
    user = await session.execute(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='Пользователь не найден!'
        )
    return user

async def get_user_by_email(email : EmailStr, session : AsyncSession = Depends(get_async_session)):
    """Получение пользователя из БД по его email"""
    user = await session.execute(select(User).where(User.email == email))
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='Пользователь не найден!'
        )
    return user

async def authenticate_user(email: str, password: str):
    """проверка правильности введенных учетных данных"""
    user = await get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
