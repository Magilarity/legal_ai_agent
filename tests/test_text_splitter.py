def test_split_text(splitter_module):
    text = "A " + "x" * 1000
    chunks = splitter_module.split_text(text, max_length=500)
    assert all(len(c) <= 500 for c in chunks)
    assert "".join(chunks) == text
