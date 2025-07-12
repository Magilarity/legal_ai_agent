# tests/unit/test_prozorro_loader_detailed.py
import importlib

import pytest

mod = pytest.importorskip("interface.prozorro_loader")


def test_prozorro_loader_import():
    assert mod


@pytest.mark.parametrize("timeout,raises", [(True, True), (False, False)])
def test_prozorro_fetch(monkeypatch, timeout, raises):
    # Assume fetch_tenders(endpoint, timeout) exists
    func = getattr(mod, "fetch_tenders", None)
    if not callable(func):
        pytest.skip("fetch_tenders not found", allow_module_level=True)
    if timeout:
        monkeypatch.setattr(
            "requests.get", lambda *a, **k: (_ for _ in ()).throw(Exception("timeout"))
        )
        with pytest.raises(Exception):
            func("http://fake", timeout=1)
    else:

        class Resp:
            status_code = 200

        Resp.json = lambda self: {"data": []}
        monkeypatch.setattr("requests.get", lambda *a, **k: Resp())
        result = func("http://fake", timeout=1)
        assert isinstance(result, list)
