# tests/unit/test_ingest_tenders_extra.py
import pytest

# Імпортуємо модуль ingest.tenders
import ingest.tenders as mod

# Знаходимо функцію load_tenders
load_fn = getattr(mod, "load_tenders", None)
if not callable(load_fn):
    pytest.skip("load_tenders not found in ingest.tenders", allow_module_level=True)


# Клас для фейкових записів з атрибутами id та value
class DummyRec:
    def __init__(self, id, value):
        self.id = id
        self.value = value


# Фейковий Session, що повертає два записи
class DummySession:
    def query(self, model):
        class Q:
            def all(self):
                return [DummyRec(1, "a"), DummyRec(2, "b")]

        return Q()

    def close(self):
        pass


@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    # Патчимо Session у модулі mod на DummySession
    monkeypatch.setattr(mod, "Session", lambda: DummySession())


def test_load_tenders_returns_records():
    result = load_fn()
    assert isinstance(result, list)
    assert len(result) == 2
    # Перевіряємо, що кожен запис має id і value
    assert all(hasattr(r, "id") and hasattr(r, "value") for r in result)


def test_load_tenders_empty(monkeypatch):
    # Фейкова сесія без записів
    class EmptySession:
        def query(self, model):
            class Q:
                def all(self):
                    return []

            return Q()

        def close(self):
            pass

    monkeypatch.setattr(mod, "Session", lambda: EmptySession())
    result = load_fn()
    assert result == []
