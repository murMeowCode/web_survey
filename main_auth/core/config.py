"""конфигурационный файл для сервиса"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """описание полей настроек"""
    database_url : str
    secret : str

    class Config:
        """путь к файлу среды"""
        env_file = '.env'
