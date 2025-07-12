# tests/unit/test_ingest_loader_advanced.py
import importlib
import json

import pytest

ldr_mod = pytest.importorskip("ingest.loader")
load_fn = next(
    (getattr(ldr_mod, n) for n in dir(ldr_mod) if n.startswith("load_")), None
)
if not load_fn:
    pytest.skip("No load_ function", allow_module_level=True)


class PageResp:
    def __init__(self, data, next_page):
        self._data = data
        self.next_page = next_page
        self.status_code = 200

    def json(self):
        return {"data": self._data, "next_page": self.next_page}


@pytest.fixture(autouse=True)
def patch_pagination(monkeypatch):
    # Sequence of pages: first [1,2], next [3], then end
    seq = [PageResp([1, 2], True), PageResp([3], False)]
    monkeypatch.setattr("requests.get", lambda *a, **k: seq.pop(0))
    return None


def test_pagination_aggregates_all():
    result = load_fn(endpoint="items", page=1, limit=2)
    assert isinstance(result, list)
    assert result == [1, 2, 3]


def test_incorrect_json_type_raises(monkeypatch):
    # Return JSON where data is not list
    class Bad:
        def __init__(self):
            self.status_code = 200

        def json(self):
            return {"data": "not a list"}

    monkeypatch.setattr("requests.get", lambda *a, **k: Bad())
    with pytest.raises(TypeError):
        load_fn()
