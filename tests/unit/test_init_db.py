# tests/unit/test_init_db.py
import sys
import types
import pytest
from sqlalchemy import create_engine

# Mock pydantic_settings and app.config
pyd = types.ModuleType("pydantic_settings")
pyd.BaseSettings = object
pyd.SettingsConfigDict = {}
sys.modules["pydantic_settings"] = pyd
appcfg = types.ModuleType("app.config")
appcfg.settings = types.SimpleNamespace(database_url="sqlite:///:memory:")
sys.modules["app.config"] = appcfg

from db.schema import Session, engine


def test_session_and_engine(tmp_path):
    # Engine should connect to in-memory or fallback
    engine2 = create_engine("sqlite:///:memory:")
    sess = Session()
    assert sess.bind == engine or sess.bind.engine == engine
    sess.close()
