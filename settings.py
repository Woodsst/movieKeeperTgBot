from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../../Desktop/app/.env", env_file_encoding="utf-8", extra="ignore"
    )
    SERVICE_ACCOUNT_FILE: str = Field()
    SPREADSHEET_ID: str = Field()
    TOKEN: str = Field()
    USERS: List = Field()
    KINOPOISK_X_API_KEY: str = Field()
    KINOPOISK_SEARCH_URL: str = Field()

s = Settings()
