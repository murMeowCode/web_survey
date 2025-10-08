"""Эндпоинты для аутентификации"""
#pylint: disable=W0621
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.core.database import get_async_session
from main_auth.core.jwt_logic import (create_access_token, create_refresh_token,
                                      get_user_by_id, authenticate_user)
from main_auth.schemas.token import AccessToken, TokenPair
from main_auth.core.config import Settings
from main_auth.schemas.user import UserCreate, UserRead
from main_auth.crud.user import create_user

router = APIRouter(prefix='/auth',tags=['auth'])

@router.post("/jwt/login", response_model=TokenPair)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session : AsyncSession = Depends(get_async_session)):
    """Получение токенов доступа при аутентификации"""
    user = await authenticate_user(form_data.username, form_data.password,session)

    access_token_expires = timedelta(minutes=Settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

@router.post("/jwt/refresh", response_model=AccessToken)
async def refresh_token(refresh_token: str, session : AsyncSession = Depends(get_async_session)):
    """Логика получения нового токена доступа"""
    try:
        payload = jwt.decode(refresh_token, Settings().secret_key,
                             algorithms=[Settings().algorithm])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user = await get_user_by_id(user_id,session)

        access_token_expires = timedelta(minutes=Settings().access_token_expire_minutes)
        new_access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": new_access_token,
        }
    except JWTError as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token") from exc

@router.post("/register", response_model=UserRead)
async def register(user_data : UserCreate, session : AsyncSession = Depends(get_async_session)):
    """Регистрация нового пользователя"""
    user = await create_user(session=session,user_data=user_data)
    return user
