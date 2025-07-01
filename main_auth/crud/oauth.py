"""Модуль для работы с пользователями от сторонней регистрации"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.models.user import User
from main_auth.schemas.oauth import OAuthUserResponse
from main_auth.crud.user import get_password_hash

async def get_or_create_oauth_user(
    session: AsyncSession,
    oauth_user: OAuthUserResponse,
) -> User:
    """Находит или создает пользователя на основе OAuth данных"""
    if oauth_user.email:
        query = select(User).where(User.email == oauth_user.email)
        result = await session.execute(query)
        user = result.scalars().first()

        if user:
            return user

    new_user = User(
        email=oauth_user.email or f"{oauth_user.provider}_{oauth_user.provider_id}@temp.domain",
        hashed_password=get_password_hash(""),  # Обязательное поле
        is_active=True,
        is_superuser=False,
        is_verified=True  # OAuth-пользователи считаются верифицированными
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
