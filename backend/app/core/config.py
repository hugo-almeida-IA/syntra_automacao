from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = "Syntra Chatbot API"
    APP_ENV: str = "development"
    DEBUG: bool = False
    SQL_ECHO: bool = False
    OLLAMA_HOST: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3"
    OLLAMA_TIMEOUT_SECONDS: float = 60.0
    CHAT_HISTORY_LIMIT: int = Field(default=20, ge=1, le=100)

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()