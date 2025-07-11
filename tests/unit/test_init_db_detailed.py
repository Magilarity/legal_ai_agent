# tests/unit/test_init_db_detailed.py
import sys, types, importlib
import pytest
from sqlalchemy.exc import OperationalError

# моки для pydantic_settings та app.config
pyd = types.ModuleType("pydantic_settings")
pyd.BaseSettings = object
pyd.SettingsConfigDict = {}
sys.modules["pydantic_settings"] = pyd
appcfg = types.ModuleType("app.config")
appcfg.settings = types.SimpleNamespace(database_url="postgresql://invalid")
sys.modules["app.config"] = appcfg

import db.schema as schema_mod


def test_schema_fallback_to_sqlite(monkeypatch):
    monkeypatch.setattr(
        schema_mod,
        "create_engine",
        lambda url, echo=False: (_ for _ in ()).throw(
            OperationalError("msg", "params", "orig")
        ),
    )
    importlib.reload(schema_mod)
    eng = schema_mod.ENGINE
    assert "sqlite" in str(eng.url)


def test_session_bind_to_engine():
    sess = schema_mod.Session()
    assert sess.bind is schema_mod.ENGINE
    sess.close()
