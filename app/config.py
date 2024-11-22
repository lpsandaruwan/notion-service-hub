from pydantic_settings import BaseSettings
from uvicorn.config import LOG_LEVELS


class Settings(BaseSettings):
    NOTION_BASE_URL: str
    NOTION_API_KEY: str
    NOTION_VERSION: str = "2022-06-28"
    APP_API_KEY: str
    LOGGING_LEVEL: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
