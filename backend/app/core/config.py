from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = ROOT_DIR / ".env",


class Settings(BaseSettings):
    APP_NAME: str = "My API"

    DATABASE_URL: str
    TEST_DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore"
    )


settings = Settings()
