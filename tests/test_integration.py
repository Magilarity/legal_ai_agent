# tests/test_integration.py


def test_end_to_end(tmp_path, loader_module, splitter_module):
    # End-to-end example: load, split, and reconstruct a document
    sample = "End to end test of the legal AI agent."
    f = tmp_path / "sample.txt"
    f.write_text(sample)
    text = loader_module.extract_text_from_file(str(f))
    chunks = splitter_module.split_text(text, max_length=50)
    combined = "".join(chunks)
    assert combined == sample
