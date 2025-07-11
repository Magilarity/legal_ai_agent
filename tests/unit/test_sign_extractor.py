# tests/unit/test_sign_extractor.py
import pytest

try:
    from app.sign_extractor import extract_signatures
except ImportError:
    pytest.skip("extract_signatures not in app.sign_extractor", allow_module_level=True)


def test_extract_signatures_empty(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("")
    res = extract_signatures(str(file))
    assert isinstance(res, list)
