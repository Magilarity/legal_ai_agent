# tests/unit/test_llm_and_config.py

import logging
import sys
import types

import pytest

# ——————————————————————————————————————————————————————————————
# Мокаємо pydantic_settings, щоб Settings-клас із app.settings імпортувався без помилок
pyd_mod = types.ModuleType("pydantic_settings")


class DummyBaseSettings:
    def __init__(self, *args, **kwargs):
        pass


class DummySettingsConfigDict:
    def __init__(self, *args, **kwargs):
        pass


pyd_mod.BaseSettings = DummyBaseSettings
pyd_mod.SettingsConfigDict = DummySettingsConfigDict
sys.modules["pydantic_settings"] = pyd_mod
# ——————————————————————————————————————————————————————————————

# Тепер імпортуємо без помилок
from app.settings import Settings


def test_settings_reads_env(monkeypatch):
    """
    Перевіряє, що Settings читає OPENAI_API_KEY з оточення.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "key123")
    settings = Settings()
    assert hasattr(settings, "OPENAI_API_KEY"), "Settings має містити OPENAI_API_KEY"
    assert settings.OPENAI_API_KEY == "key123"


# ——————————————————————————————————————————————————————————————
# Тест get_config (якщо є в app.config)
# ——————————————————————————————————————————————————————————————
try:
    from app.config import get_config
except ImportError:
    pytest.skip(
        "get_config не знайдено в app.config — пропускаємо відповідні тести",
        allow_module_level=True,
    )
else:

    def test_get_config(monkeypatch):
        """
        Перевіряє, що get_config() читає APP_ENV з оточення.
        """
        monkeypatch.setenv("APP_ENV", "prod")
        cfg = get_config()
        assert hasattr(cfg, "ENV"), "Config має містити атрибут ENV"
        assert cfg.ENV == "prod"


# ——————————————————————————————————————————————————————————————
# Тест setup_logging
# ——————————————————————————————————————————————————————————————
from app.logging_config import setup_logging


def test_setup_logging_creates_handler(tmp_path, monkeypatch):
    """
    Перевіряє, що setup_logging() додає хоча б один файловий обробник.
    """
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    setup_logging()

    handlers = logging.getLogger().handlers
    # FileHandler має атрибут baseFilename
    file_handlers = [h for h in handlers if hasattr(h, "baseFilename")]
    assert file_handlers, "Не знайдено FileHandler у кореневому логері"


# ——————————————————————————————————————————————————————————————
# Тест LLMAgent через OpenAI SDK (якщо SDK встановлено)
# ——————————————————————————————————————————————————————————————
openai = pytest.importorskip(
    "openai", reason="OpenAI SDK is required for LLMAgent tests"
)

try:
    from app.llm_agent import LLMAgent
except ImportError:
    pytest.skip(
        "LLMAgent не знайдено в app.llm_agent — пропускаємо тести агента",
        allow_module_level=True,
    )
else:

    def test_llm_agent_calls_openai(monkeypatch):
        """
        Перевіряє, що LLMAgent при виклику chat() використовує openai.ChatCompletion.create().
        """
        calls = []

        # Заготовка для ChatCompletion.create
        def dummy_create(**kwargs):
            calls.append(kwargs)
            return {"choices": [{"message": {"content": "OK"}}]}

        # Мокаємо метод create у ChatCompletion
        monkeypatch.setattr(
            openai.ChatCompletion, "create", dummy_create, raising=False
        )

        agent = LLMAgent(api_key="fake_key", model="gpt-test")
        response = agent.chat("Hello")

        assert response == "OK", "Невірний вміст відповіді від LLMAgent"
        assert calls, "LLMAgent не викликав openai.ChatCompletion.create()"
        assert (
            calls[0].get("model") == "gpt-test"
        ), "Агент передав неправильне ім'я моделі"
