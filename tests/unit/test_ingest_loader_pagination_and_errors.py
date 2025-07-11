import pytest
from requests.exceptions import HTTPError, Timeout

# Імпортуємо нашу функцію
from ingest.loader import load_documents


class PageResp:
    def __init__(self, data, next_page, status_code=200):
        self._data = data
        self.next_page = next_page
        self.status_code = status_code

    def json(self):
        return {"data": self._data, "next_page": self.next_page}


@pytest.fixture(autouse=True)
def patch_requests(monkeypatch):
    # Готуємо дві сторінки: [1,2] → next_page=True, потім [3] → next_page=False
    seq = [PageResp([1, 2], True), PageResp([3], False)]
    monkeypatch.setattr("ingest.loader.requests.get", lambda *a, **k: seq.pop(0))


def test_pagination_aggregation():
    result = load_documents(endpoint="items", page=1, limit=2)
    assert result == [1, 2, 3]


@pytest.mark.parametrize("status_code", [400, 500])
def test_http_error_raises(monkeypatch, status_code):
    class BadResp:
        def __init__(self, code):
            self.status_code = code

        def raise_for_status(self):
            raise HTTPError(f"HTTP {self.status_code}")

    monkeypatch.setattr(
        "ingest.loader.requests.get", lambda *a, **k: BadResp(status_code)
    )
    with pytest.raises(HTTPError):
        load_documents(endpoint="items")


def test_invalid_json_type_raises(monkeypatch):
    class BadJSON:
        status_code = 200

        def json(self):
            return {"data": "not a list", "next_page": False}

    monkeypatch.setattr("ingest.loader.requests.get", lambda *a, **k: BadJSON())
    with pytest.raises(TypeError):
        load_documents(endpoint="items")


def test_timeout_raises(monkeypatch):
    monkeypatch.setattr(
        "ingest.loader.requests.get", lambda *a, **k: (_ for _ in ()).throw(Timeout())
    )
    with pytest.raises(Timeout):
        load_documents(endpoint="items")
