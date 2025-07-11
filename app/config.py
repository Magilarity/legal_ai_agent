from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import subprocess
import shutil


class Settings(BaseSettings):
    # читаем .env и валидируем при присвоении
    model_config = SettingsConfigDict(env_file=".env", validate_assignment=True)

    openai_api_key: str = Field(..., env="OPENAI_API_KEY")  # type: ignore[call-overload]
    database_url: str = Field(..., env="DATABASE_URL")  # type: ignore[call-overload]
    slack_api_url: str = Field(..., env="SLACK_API_URL")  # type: ignore[call-overload]


# пытаемся запустить Vault Agent, если он есть в PATH
if shutil.which("vault"):
    try:
        vault_proc = subprocess.Popen(
            ["vault", "agent", "-config=monitoring/vault-agent.hcl"]
        )
    except Exception as e:
        print(f"⚠️ Не удалось запустить Vault Agent: {e}")
else:
    print("ℹ️ Vault binary не найдено. Пропускаем запуск Vault Agent.")

# инстанцируем
settings = Settings()  # type: ignore[call-arg]
