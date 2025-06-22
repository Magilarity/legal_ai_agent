from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str

    class Config:
        env_file = ".env"
