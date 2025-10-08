"""crud operations for user"""
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib import context
from main_auth.schemas.user import UserRead
from main_auth.models.user import User

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """Хэширование пароля"""
    return pwd_context.hash(password)

async def create_user(session: AsyncSession, user_data: dict) -> UserRead:
    """Создание нового пользователя"""
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

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

async def update_user_info(new_data, current_user, session: AsyncSession):
    """Изменение информации о пользователе"""
    update_data = new_data.dict(exclude_unset=True)

    print(f"Updating with: {update_data}")  # Для отладки

    for field, value in update_data.items():
        if hasattr(current_user, field):
            setattr(current_user, field, value)

    if 'password' in update_data:
        current_user.hashed_password = get_password_hash(update_data['password'])

    await session.commit()
    await session.refresh(current_user)
    return current_user
