def test_extract_text_from_file(tmp_path, loader_module):
    f = tmp_path / "test.txt"
    f.write_text("Hello world")
    text = loader_module.extract_text_from_file(str(f))
    assert text == "Hello world"
