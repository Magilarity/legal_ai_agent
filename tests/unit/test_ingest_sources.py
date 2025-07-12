# tests/unit/test_ingest_sources_detailed.py
import importlib

import pytest
import requests
from requests.exceptions import Timeout

# Список ingest-модулів для тестування
MODULES = [
    "ingest.acts",
    "ingest.consultations",
    "ingest.decisions",
]


@pytest.mark.parametrize(
    "module_name,status_code,json_data,expect_empty",
    [
        ("ingest.acts", 200, {"data": [{"x": 1}]}, False),
        ("ingest.acts", 200, {"data": []}, True),
        ("ingest.consultations", 200, {"data": [{"y": 2}]}, False),
        ("ingest.consultations", 200, {"data": []}, True),
        ("ingest.decisions", 200, {"data": [{"z": 3}]}, False),
        ("ingest.decisions", 200, {"data": []}, True),
    ],
)
def test_ingest_loader_success(
    monkeypatch, module_name, status_code, json_data, expect_empty
):
    # Імпортуємо модуль
    mod = importlib.import_module(module_name)
    # Знаходимо першу функцію, що починається з load_
    load_fn = next(
        (getattr(mod, name) for name in dir(mod) if name.startswith("load_")), None
    )
    if load_fn is None:
        pytest.skip(f"No load_ function in {module_name}", allow_module_level=True)

    # Створюємо мок-Response
    class Resp:
        def __init__(self, code, data):
            self.status_code = code
            self._data = data

        def json(self):
            return self._data

    # Підмінюємо requests.get
    monkeypatch.setattr(
        requests, "get", lambda *args, **kwargs: Resp(status_code, json_data)
    )

    # Виклик loader-функції без параметрів
    result = load_fn()
    assert isinstance(result, list)
    if expect_empty:
        assert result == []
    else:
        assert result, "Expected non-empty result"


@pytest.mark.parametrize("module_name", MODULES)
def test_ingest_loader_timeout(monkeypatch, module_name):
    # Імпортуємо модуль
    mod = importlib.import_module(module_name)
    load_fn = next(
        (getattr(mod, name) for name in dir(mod) if name.startswith("load_")), None
    )
    if load_fn is None:
        pytest.skip(f"No load_ function in {module_name}", allow_module_level=True)

    # Підмінюємо requests.get, щоб він кидал Timeout
    monkeypatch.setattr(
        requests,
        "get",
        lambda *args, **kwargs: (_ for _ in ()).throw(Timeout("timeout")),
    )

    with pytest.raises(Exception):
        load_fn()
