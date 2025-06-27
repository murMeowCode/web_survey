"""Схемы описания токенов"""
from pydantic import BaseModel

class AccessToken(BaseModel):
    """Схема для возвращения токена доступа"""
    access_token: str

class TokenPair(BaseModel):
    """Схема для возвращения токенов"""
    refresh_token: str | None = None
