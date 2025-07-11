# tests/unit/test_interface_smoke.py
import pytest
import importlib


@pytest.mark.parametrize(
    "mod", ["interface.prozorro_loader", "interface.streamlit_app"]
)
def test_interface_importable(mod):
    m = importlib.import_module(mod)
    assert m, f"Module {mod} failed to import"
