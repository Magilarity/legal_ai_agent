# tests/unit/test_init_db_core.py
import sys
import types
import pytest
from sqlalchemy import inspect

# Мокаємо pydantic_settings та app.config для in-memory SQLite
pyd = types.ModuleType("pydantic_settings")
pyd.BaseSettings = object
pyd.SettingsConfigDict = {}
sys.modules["pydantic_settings"] = pyd
appcfg = types.ModuleType("app.config")
appcfg.settings = types.SimpleNamespace(database_url="sqlite:///:memory:")
sys.modules["app.config"] = appcfg

# Імпортуємо схему та функцію init_db
import db.schema as schema_mod
import db.init_db as init_mod


def test_init_db_function_creates_tables():
    """
    Перевіряє, що init_db створює всі таблиці, перелічені в schema_mod.TABLES.
    """
    # Підключаємось та створюємо таблиці через init_db
    conn = schema_mod.engine.connect()
    try:
        # Викликаємо функцію init_db, може вимагати conn або не вимагати аргумент
        try:
            init_mod.init_db(conn=conn)
        except TypeError:
            init_mod.init_db()
    finally:
        conn.close()

    # Перевіряємо таблиці за допомогою інспектора
    inspector = inspect(schema_mod.engine)
    tables = inspector.get_table_names()
    for tbl in schema_mod.TABLES:
        assert tbl in tables, f"Missing table {tbl}"


def test_session_bound_to_engine():
    """
    Перевіряє, що Session() з schema_mod прив'язана до правильного engine.
    """
    from db.schema import Session as SchemaSession

    sess = SchemaSession()
    assert (
        sess.bind is schema_mod.engine
    ), "Session має бути прив'язана до schema_mod.engine"
    sess.close()
