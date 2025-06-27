"""routers for users ops"""
#pylint: disable=W0621
from datetime import timedelta
from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.core.database import get_async_session
from main_auth.core.jwt_logic import authenticate_user
from main_auth.core.auth import fastapi_users
from main_auth.core.jwt_logic import create_access_token, create_refresh_token, get_user_by_id
from main_auth.schemas.user import UserCreate, UserRead, UserUpdate
from main_auth.schemas.token import AccessToken, TokenPair
from main_auth.core.config import Settings

router = APIRouter()

@router.post("/auth/jwt/login", response_model=TokenPair, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session : AsyncSession = Depends(get_async_session)):
    """Получение токенов доступа при аутентификации"""
    user = await authenticate_user(form_data.username, form_data.password,session)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Settings().access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

@router.post("/auth/jwt/refresh", response_model=AccessToken, tags=["auth"])
async def refresh_token(refresh_token: str, session : AsyncSession = Depends(get_async_session)):
    """Логика получения нового токена доступа"""
    try:
        payload = jwt.decode(refresh_token, Settings().secret_key,
                             algorithms=[Settings().algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user = await get_user_by_id(user_id,session)

        access_token_expires = timedelta(minutes=Settings().access_token_expire_minutes)
        new_access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        return {
            "access_token": new_access_token,
        }
    except JWTError as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token") from exc

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users']
)

@router.delete('/users/{id}', tags=['users'], deprecated=True)
def delete_user(id: int):  #pylint: disable=W0622
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=405,
        detail="Удаление пользователей запрещено!"
    )
