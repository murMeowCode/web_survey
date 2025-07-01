"""конфигурационный файл для сервиса"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """описание полей настроек"""
    database_url : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    refresh_token_expire_days : int
    nats_url : str

    class Config:
        """путь к файлу среды"""
        env_file = '.env'
