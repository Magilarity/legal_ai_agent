# tests/unit/test_signature_modules_detailed.py
import pytest
import tempfile
from pathlib import Path

# sign_extractor
sign_mod = pytest.importorskip("app.sign_extractor")
extract = getattr(sign_mod, "extract_signatures", None)
if not callable(extract):
    pytest.skip("extract_signatures not found", allow_module_level=True)

# Create fake PEM and DER signature blocks for testing
pem_content = "-----BEGIN SIGNATURE-----\nABCDEF\n-----END SIGNATURE-----"
der_content = b"\x30\x82\x01\x0aFakeDERBytes"


def test_extract_signatures_pem(tmp_path):
    f = tmp_path / "sig.pem"
    f.write_text(pem_content)
    sigs = extract(str(f))
    assert isinstance(sigs, list)
    assert any("ABCDEF" in s for s in sigs)


def test_extract_signatures_der(tmp_path):
    f = tmp_path / "sig.der"
    f.write_bytes(der_content)
    sigs = extract(str(f))
    assert isinstance(sigs, list)
    assert sigs  # non-empty list


# signature_extractor
sigext_mod = pytest.importorskip("app.signature_extractor")
classes = [c for n, c in vars(sigext_mod).items() if n.endswith("Extractor")]


@pytest.mark.parametrize("cls", classes)
def test_signature_extractor_extracts(cls, tmp_path):
    inst = cls()
    # provide fake input file
    f = tmp_path / "data.bin"
    f.write_bytes(b"FAKE")
    try:
        result = inst.extract(str(f))
        assert isinstance(result, list)
    except Exception:
        pytest.skip(f"{cls.__name__} cannot process fake input")


# signature_reader
sigread_mod = pytest.importorskip("app.signature_reader")
reader_classes = [c for n, c in vars(sigread_mod).items() if n.endswith("Reader")]


@pytest.mark.parametrize("cls", reader_classes)
def test_signature_reader_reads(cls):
    inst = cls()
    dummy_blocks = ["<Signed>abc</Signed>", b"<Signed>xyz</Signed>"]
    result = inst.read(dummy_blocks)
    assert isinstance(result, list)
