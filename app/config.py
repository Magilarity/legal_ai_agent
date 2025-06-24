# mypy: disable-error-code="valid-type,misc"
from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str
