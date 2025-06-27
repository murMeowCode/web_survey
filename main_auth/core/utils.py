"""вспомогательные функции"""
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.models.user import User

async def get_user_by_id(user_id : int, session : AsyncSession):
    """Получение пользователя из БД по его id"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail='Пользователь не найден!'
        )
    return user

async def get_user_by_email(email: EmailStr, session: AsyncSession):
    """Получение пользователя из БД по его email"""
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()  # Get the first result or None

    if user is None:
        raise HTTPException(
            status_code=404,
            detail='Пользователь не найден!'
        )
    return user
