"""модуль для описания схем OAuth"""
from pydantic import BaseModel

class GoogleAuthRequest(BaseModel):
    """Запросный токен от Гугл"""
    token: str  # Google ID Token (JWT)

class OAuthUserResponse(BaseModel):
    """Общий шаблон для ответа сервиса"""
    provider: str  # "google"
    provider_id: str  # "123456789"
    email: str | None
    name: str | None
    avatar: str | None
