# tests/unit/test_streamlit_app.py
import pytest

mod = pytest.importorskip("interface.streamlit_app")


def test_streamlit_app_smoke():
    # Імпорт модуля та ключових функцій
    assert hasattr(mod, "download_documents"), "download_documents missing"
    assert callable(mod.download_documents)
    assert hasattr(mod, "init_metrics"), "init_metrics missing"
    # Виклик init_metrics
    mod.init_metrics(port=8005)
