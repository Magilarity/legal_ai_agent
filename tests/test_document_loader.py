import pytest
from app.document_loader import DocumentLoader


@pytest.fixture
def tmp_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    return str(f)


def test_load_empty_raises(tmp_empty_file):
    loader = DocumentLoader()
    with pytest.raises(ValueError):
        loader.load(tmp_empty_file)


def test_load_simple_text(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("Привіт, світ!")
    loader = DocumentLoader()
    docs = loader.load(str(f))
    assert isinstance(docs, list)
    assert docs[0].page_content.startswith("Привіт")
