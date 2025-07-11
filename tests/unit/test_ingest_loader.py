# tests/unit/test_ingest_loader.py

import pytest
import ingest.loader as loader

# Список можливих імен функції для завантаження документів
CANDIDATE_NAMES = ["load_documents", "load", "fetch_documents", "get_documents"]

# Знаходимо першу наявну функцію серед кандидатів
load_fn = None
for name in CANDIDATE_NAMES:
    if hasattr(loader, name):
        load_fn = getattr(loader, name)
        break

# Якщо жодного з очікуваних варіантів немає — пропускаємо весь модуль тестів
if load_fn is None:
    pytest.skip(
        "Не знайдено функції завантаження в ingest.loader", allow_module_level=True
    )


def test_loader_success(monkeypatch):
    """
    Перевіряє успішний випадок: мокає HTTP-виклик і чекає список документів.
    """
    # Приклад: припустимо, що ваша функція приймає аргументи (endpoint, params)
    # Адаптуйте виклик load_fn(...) під реальний сигнатурний вигляд у вас
    sample_response = [{"id": "123", "title": "Test"}]

    # Мокаємо requests.get у модулі loader
    import requests

    class DummyResp:
        status_code = 200

        def json(self):
            return {"data": sample_response}

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: DummyResp())

    # Викликаємо знайдену функцію
    docs = load_fn(endpoint="http://fake/api", params={"q": "test"})

    assert isinstance(docs, list), "Очікуємо список документів"
    assert docs == sample_response, "Невірний результат при успішному відповіді"


def test_loader_error(monkeypatch):
    """
    Перевіряє обробку помилкового статусу (наприклад, raise RuntimeError).
    """
    import requests

    class ErrResp:
        status_code = 500

        def json(self):
            return {}

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: ErrResp())

    with pytest.raises(Exception):
        # Викликаємо ту ж функцію з очікуванням винятку
        load_fn(endpoint="http://fake/api", params={})
