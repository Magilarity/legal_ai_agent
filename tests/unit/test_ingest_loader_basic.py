import pytest

from ingest.loader import download_documents, process_sheet


# Dummy worksheet for testing
class DummySheet:
    def __init__(self):
        self.title = "Sheet1"
        self.rows = []

    def append(self, row):
        self.rows.append(row)


def test_download_documents_success():
    # Без помилки повертається шлях
    result = download_documents("tender123")
    assert result == "downloads/123"


def test_download_documents_error():
    # При error=True повертається None
    result = download_documents("tender123", error=True)
    assert result is None


def test_process_sheet_valid():
    ws = DummySheet()
    # Виклик не повинен кидати помилок
    process_sheet(ws)
    # Після виклику лист має один пустий рядок
    assert ws.rows == [[]]
    # Назва листа залишається незмінною
    assert ws.title == "Sheet1"


def test_process_sheet_none():
    # Передача None призводить до AssertionError
    with pytest.raises(AssertionError):
        process_sheet(None)
