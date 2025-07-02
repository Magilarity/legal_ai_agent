from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import subprocess
import shutil


class Settings(BaseSettings):
    # Читаємо з .env та валідуємо при присвоєнні
    model_config = SettingsConfigDict(env_file=".env", validate_assignment=True)

    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    database_url: str = Field(..., env="DATABASE_URL")
    slack_api_url: str = Field(..., env="SLACK_API_URL")


# Спроба запустити Vault Agent, якщо бінарний файл доступний
if shutil.which("vault"):
    try:
        vault_proc = subprocess.Popen(
            ["vault", "agent", "-config=monitoring/vault-agent.hcl"]
        )
    except Exception as e:
        print(f"⚠️ Не вдалося запустити Vault Agent: {e}")
else:
    print("ℹ️ Vault binary не знайдено. Пропускаємо запуск Vault Agent.")


# Інстанціювання налаштувань
settings = Settings()
