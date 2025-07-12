# tests/unit/test_db_schema.py

import sys
import types

import pytest
from sqlalchemy import create_engine, text

# ——————————————————————————————————————————————————————————————
# Мокаємо pydantic_settings, щоб Settings із app.settings імпортувався без помилок
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

# Мокаємо app.config.settings із in-memory SQLite URL
app_config = types.ModuleType("app.config")
app_config.settings = types.SimpleNamespace(database_url="sqlite:///:memory:")
sys.modules["app.config"] = app_config
# ——————————————————————————————————————————————————————————————

from db.schema import TABLES, Base


def test_schema_creates_all_tables():
    """
    Перевіряє, що при створенні метаданих SQLAlchemy
    (Base.metadata.create_all) у in-memory SQLite з'являються
    всі таблиці, перелічені в TABLES.
    """
    # Створюємо in-memory БД і таблиці за метаданими
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    # Виконуємо raw SQL через text()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        existing_tables = {row[0] for row in result.fetchall()}

    # Перевіряємо, що всі очікувані таблиці присутні
    missing = [tbl for tbl in TABLES if tbl not in existing_tables]
    assert not missing, f"Не знайдено таблиць: {missing}"
