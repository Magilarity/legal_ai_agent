# tests/unit/test_vector_store.py

import pytest
import numpy as np

# Пропускаємо тест, якщо faiss не встановлений
faiss = pytest.importorskip(
    "faiss", reason="Faiss library is required for vector store tests"
)

from app.vector_store import search_index


@pytest.fixture
def index_fixture():
    d = 4
    # Генеруємо 10 випадкових векторів
    xb = np.random.random((10, d)).astype("float32")
    index = faiss.IndexFlatL2(d)
    index.add(xb)
    return index, xb


def test_search_index_returns_correct_length(index_fixture):
    index, xb = index_fixture
    # Питання — перший вектор
    q = xb[0].tolist()
    topk = 5
    result = search_index(index, q, top_k=topk)

    assert isinstance(result, list), "search_index має повертати список"
    assert len(result) == topk, f"Очікуємо {topk} індексів, отримали {len(result)}"


def test_search_index_returns_valid_indices(index_fixture):
    index, xb = index_fixture
    # Питання — другий вектор (саме собі найменша відстань)
    q = xb[1].tolist()
    result = search_index(index, q, top_k=3)

    # Перевіряємо тип і діапазон
    assert all(isinstance(i, int) for i in result), "Всі індекси мають бути int"
    assert all(
        0 <= i < index.ntotal for i in result
    ), "Індекси мають бути в межах [0, ntotal)"

    # Перший елемент має бути self-match (тобто індекс 1)
    assert (
        result[0] == 1
    ), "Найближчий вектор до самого себе має бути першим результатом"
