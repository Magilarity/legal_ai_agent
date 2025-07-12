# tests/unit/test_signature_reader.py
import importlib

import pytest

reader_mod = importlib.import_module("app.signature_reader")
readers = [getattr(reader_mod, n) for n in dir(reader_mod) if n.endswith("Reader")]
if not readers:
    pytest.skip("No Reader classes in app.signature_reader", allow_module_level=True)


@pytest.mark.parametrize("cls", readers)
def test_signature_reader_has_read(cls):
    inst = cls()
    assert hasattr(inst, "read"), f"{cls.__name__} missing read()"
