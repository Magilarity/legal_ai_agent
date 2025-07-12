# tests/unit/test_signature_extractor.py
import importlib

import pytest

sigext = importlib.import_module("app.signature_extractor")
classes = [getattr(sigext, n) for n in dir(sigext) if n.endswith("Extractor")]
if not classes:
    pytest.skip(
        "No Extractor classes in app.signature_extractor", allow_module_level=True
    )


@pytest.mark.parametrize("cls", classes)
def test_signature_extractor_has_extract(cls):
    inst = cls()
    assert hasattr(inst, "extract"), f"{cls.__name__} missing extract()"
