from pydantic import BaseSettings, Field
from pathlib import Path
import subprocess


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    database_url: str = Field(..., env="DATABASE_URL")
    slack_api_url: str = Field(..., env="SLACK_API_URL")

    class Config:
        validate_assignment = True


# перед інстанціюванням вишукаємо секрети з Vault
vault_token = subprocess.run(
    ["vault", "agent", "-config=monitoring/vault-agent.hcl"], capture_output=True
)
# після старту Vault Agent середовище наповниться

settings = Settings()
