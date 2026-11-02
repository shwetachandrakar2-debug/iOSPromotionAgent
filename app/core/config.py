from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # PROJECT_NAME: str = "LocalBiz AI Studio Backend"
    # API_V1_STR: str = "/api/v1"
    # ENVIRONMENT: str = "production"

    # ALLOWED_ORIGINS: List[str] = [
    #     "https://iosagent.com",
    #     "http://localhost:3000",
    #     "http://127.0.0.1:3000",
    # ]

    # GEMINI_API_KEY: str = ""
    # DEFAULT_IMAGE_WIDTH: int = 1080
    # DEFAULT_IMAGE_HEIGHT: int = 1080

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


settings = AppSettings()
