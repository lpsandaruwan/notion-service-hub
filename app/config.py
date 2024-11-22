import logging
from pydantic_settings import BaseSettings

LOGGING_LEVELS = {
    'debug': logging.DEBUG,
    'error': logging.ERROR,
    'info': logging.INFO,
    'warn': logging.WARNING
}

class Settings(BaseSettings):
    NOTION_BASE_URL: str
    NOTION_API_KEY: str
    NOTION_VERSION: str = "2022-06-28"
    APP_API_KEY: str
    LOGGING_LEVEL: str = "info"

    @property
    def logging_level(self):
        return LOGGING_LEVELS.get(self.LOGGING_LEVEL.lower(), logging.INFO)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
