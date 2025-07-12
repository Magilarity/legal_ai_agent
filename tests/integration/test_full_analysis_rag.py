# tests/integration/test_full_analysis_rag.py

from unittest.mock import MagicMock

import faiss
import numpy as np
import pytest

# Імпортуємо модуль, який тестуємо
import app.full_analysis as full


# Фікстура: створюємо простий FAISS-індекс у пам'яті
@pytest.fixture
def faiss_index(tmp_path, monkeypatch):
    # Невеликий 2-вимірний індекс
    dim = 2
    index = faiss.IndexFlatL2(dim)
    # Додаємо три вектори
    vecs = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]], dtype=np.float32)
    index.add(vecs)
    # Патчимо повертання індексу
    monkeypatch.setattr(
        full,
        "load_faiss_index",  # у full_analysis має бути функція, що повертає index
        lambda *args, **kwargs: index,
    )
    return index


# Фікстура: мок download_documents
@pytest.fixture(autouse=True)
def patch_download_documents(monkeypatch):
    docs = [
        {"id": "d1", "content": "Документ 1"},
        {"id": "d2", "content": "Документ 2"},
        {"id": "d3", "content": "Документ 3"},
    ]
    monkeypatch.setattr(full, "download_documents", lambda tender_id: docs)


# Фікстура: мок векторизатора (embedder)
@pytest.fixture(autouse=True)
def patch_embedder(monkeypatch):
    # Простий embed: кожен документ дає вектор [idx, idx]
    def fake_embedder(texts):
        return [np.array([i, i], dtype=np.float32) for i in range(len(texts))]

    monkeypatch.setattr(full, "embed_texts", fake_embedder)


# Фікстура: мок агента LLM
@pytest.fixture(autouse=True)
def patch_llm_agent(monkeypatch):
    fake_agent = MagicMock()
    fake_agent.chat.return_value = "ANALYSIS_OK"
    # Будь-який виклик LLMAgent() повертає наш fake_agent
    monkeypatch.setattr(full, "LLMAgent", lambda *args, **kwargs: fake_agent)


def test_full_analysis_rag_conveyor(faiss_index):
    """
    End-to-end інтеграція: завантажуємо документи, векторизуємо,
    шукаємо в індексі, викликаємо LLM, отримуємо фінальний string.
    """
    result = full.analyze_tender(tender_id="UA-TEST")
    # У нашій поточній реалізації analyze_tender повертає рядок із chat()
    assert isinstance(result, str)
    assert result == "ANALYSIS_OK"
