from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # читаем .env и валидируем при присвоении
    model_config = SettingsConfigDict(env_file=".env", validate_assignment=True)

    openai_api_key: str = Field(..., env="OPENAI_API_KEY")  # type: ignore[call-overload]
    database_url: str = Field(..., env="DATABASE_URL")  # type: ignore[call-overload]
    slack_api_url: str = Field(..., env="SLACK_API_URL")  # type: ignore[call-overload]


# инстанцируем — читаем значения из окружения
settings = Settings()  # type: ignore[call-arg]
