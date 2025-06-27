"""Модуль описания jwt логики"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.core.config import Settings
from main_auth.core.database import get_async_session
from main_auth.crud.user import get_user_by_email, get_user_by_id, pwd_context


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/jwt/login")

def verify_password(plain_password: str, hashed_password: str):
    """Функция проверки пароля"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Логика создания токена доступа"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Settings().secret_key, algorithm=Settings().algorithm)

def create_refresh_token(data: dict):
    """Логика создания токена обновления"""
    expire = datetime.now() + timedelta(days=Settings().refresh_token_expire_days)
    data.update({"exp": expire})
    return jwt.encode(data, Settings().secret_key, algorithm=Settings().algorithm)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Логика получения пользователя по токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Settings().secret_key, algorithms=[Settings().algorithm])
        user_id: id = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = await get_user_by_id(user_id, Depends(get_async_session))
    return user

async def authenticate_user(email: str, password: str, session : AsyncSession):
    """проверка правильности введенных учетных данных"""
    user = await get_user_by_email(email, session)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Пользователя с такой электронной почтой не существует",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Неверно введенный пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
