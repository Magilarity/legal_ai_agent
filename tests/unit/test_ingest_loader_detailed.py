# tests/unit/test_ingest_loader_detailed.py
import importlib
from inspect import signature

import pytest
import requests

ldr_mod = pytest.importorskip("ingest.loader", reason="ingest.loader required")
load_fn = next(
    (getattr(ldr_mod, n) for n in dir(ldr_mod) if n.startswith("load_")), None
)
if not load_fn:
    pytest.skip("No load_ fn", allow_module_level=True)


# порожній респонс
class EmptyResp:
    status_code = 200

    def json(self):
        return {"data": []}


def test_ingest_loader_empty(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **k: EmptyResp())
    result = load_fn(endpoint="x", params={})
    assert result == []


# пагінація
class PaginatedResp:
    def __init__(self):
        self.called = 0

    status_code = 200

    def json(self):
        self.called += 1
        return {"data": [self.called], "next_page": self.called < 2}


def test_ingest_loader_pagination(monkeypatch):
    pr = PaginatedResp()
    monkeypatch.setattr(requests, "get", lambda *a, **k: pr)
    result = load_fn(endpoint="x", params={})
    assert result == [1, 2]


# tests/unit/test_streamlit_app.py
import pytest

mod = pytest.importorskip(
    "interface.streamlit_app", reason="interface.streamlit_app required"
)


def test_streamlit_app_smoke():
    assert hasattr(mod, "download_documents")
    assert callable(mod.download_documents)
    assert hasattr(mod, "init_metrics")
    mod.init_metrics(port=8005)
