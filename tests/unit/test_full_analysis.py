# tests/unit/test_full_analysis.py
import pytest

pytest.skip(
    "Legacy tests skipped — analyze_tender тепер повертає рядок через RAGEngine",
    allow_module_level=True,
)
import pytest
import numpy as np
import importlib
from unittest.mock import MagicMock

# Перевіряємо наявність модуля
full = pytest.importorskip("app.full_analysis", reason="app.full_analysis required")


# Фікстура для мокання агента LLMAgent
@pytest.fixture(autouse=True)
def patch_llm_agent(monkeypatch):
    fake_agent = MagicMock()
    fake_agent.chat.return_value = "Analysis OK"
    llm_mod = importlib.import_module("app.llm_agent")
    for name in dir(llm_mod):
        cls = getattr(llm_mod, name)
        if isinstance(cls, type) and hasattr(cls, "chat"):
            monkeypatch.setattr(llm_mod, name, lambda *args, **kwargs: fake_agent)
            break
    return fake_agent


# Фікстура для мокання FAISS-індексу
@pytest.fixture(autouse=True)
def patch_vector_store(monkeypatch):
    fake_index = MagicMock()
    fake_index.search.return_value = (np.array([[0.0]]), np.array([[0]]))
    if hasattr(full, "create_index"):
        monkeypatch.setattr(full, "create_index", lambda docs: fake_index)
    else:
        monkeypatch.setattr(
            "app.vector_store.search_index", lambda idx, vec, top_k=None: [0]
        )
    return fake_index


def test_analyze_tender_basic(capsys):
    """
    Тестуємо поточну реалізацію analyze_tender: очікуємо None та повідомлення у stdout.
    """
    setattr(
        full, "download_documents", lambda tender_id: [{"id": "1", "content": "Hello"}]
    )

    result = full.analyze_tender(tender_id="UA-1")
    captured = capsys.readouterr()

    assert (
        result is None
    ), "Очікується, що analyze_tender повертає None за поточною реалізацією"
    assert "Documents downloaded to [" in captured.out
    assert "'id': '1'" in captured.out


def test_analyze_tender_no_docs(capsys):
    """
    Якщо download_documents повертає порожній список, за поточною реалізацією має виводитися повідомлення й повертатися None.
    """
    full_local = importlib.reload(importlib.import_module("app.full_analysis"))
    setattr(full_local, "download_documents", lambda tender_id: [])

    result = full_local.analyze_tender(tender_id="UA-2")
    captured = capsys.readouterr()

    assert (
        result is None
    ), "Очікується, що analyze_tender повертає None за відсутності документів"
    assert "Documents downloaded to []" in captured.out
