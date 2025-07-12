# tests/unit/test_signature_modules.py

import importlib
from pathlib import Path

import pytest

# Тест для модуля app.sign_extractor
try:
    sign_mod = importlib.import_module("app.sign_extractor")
    extract_fn = getattr(sign_mod, "extract_signatures", None)
    if extract_fn is None or not callable(extract_fn):
        raise ImportError
except ImportError:
    pytest.skip(
        "extract_signatures not found in app.sign_extractor", allow_module_level=True
    )
else:

    def test_extract_signatures_no_signatures(tmp_path):
        # створюємо порожній файл
        p = tmp_path / "empty.txt"
        p.write_text("")
        result = extract_fn(str(p))
        assert isinstance(result, list), "extract_signatures має повертати список"


# Тест для модуля app.signature_extractor
try:
    sigext_mod = importlib.import_module("app.signature_extractor")
    extractor_classes = [
        getattr(sigext_mod, attr)
        for attr in dir(sigext_mod)
        if attr.lower().endswith("extractor")
        and isinstance(getattr(sigext_mod, attr), type)
    ]
    if not extractor_classes:
        raise ImportError
except ImportError:
    pytest.skip(
        "No extractor classes found in app.signature_extractor", allow_module_level=True
    )
else:

    @pytest.mark.parametrize("cls", extractor_classes)
    def test_signature_extractor_interface(cls):
        inst = cls()
        # Перевіряємо наявність методу extract
        assert hasattr(inst, "extract"), f"{cls.__name__} має мати метод extract"


# Тест для модуля app.signature_reader
try:
    reader_mod = importlib.import_module("app.signature_reader")
    reader_classes = [
        getattr(reader_mod, attr)
        for attr in dir(reader_mod)
        if attr.lower().endswith("reader")
        and isinstance(getattr(reader_mod, attr), type)
    ]
    if not reader_classes:
        raise ImportError
except ImportError:
    pytest.skip(
        "No reader classes found in app.signature_reader", allow_module_level=True
    )
else:

    @pytest.mark.parametrize("cls", reader_classes)
    def test_signature_reader_interface(cls):
        inst = cls()
        # Перевіряємо наявність методу read
        assert hasattr(inst, "read"), f"{cls.__name__} має мати метод read"
