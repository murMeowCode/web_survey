"""конфигурационный файл для сервиса"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """описание полей настроек"""
    database_url : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int
    refresh_token_expire_days : int

    class Config:
        """путь к файлу среды"""
        env_file = '.env'
