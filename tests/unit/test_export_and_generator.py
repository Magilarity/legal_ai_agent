# tests/unit/test_export_and_generator.py

import pytest

from app.export_utils import another_function, build_report


def test_build_report_returns_bytes_default():
    """
    Перевіряє, що build_report повертає байти навіть без підписів.
    """
    result = build_report()
    assert isinstance(result, (bytes, bytearray))
    # може бути порожній, але тип має бути байтовим
    assert len(result) >= 0


def test_build_report_returns_bytes_with_signatures():
    """
    Перевіряє, що build_report повертає байти при передачі списку підписів.
    """
    signatures = [{"sig": "data"}]
    result = build_report(signatures)
    assert isinstance(result, (bytes, bytearray))


def test_another_function_returns_bytes_default():
    """
    Перевіряє, що another_function повертає байти навіть без підписів.
    """
    result = another_function()
    assert isinstance(result, (bytes, bytearray))


def test_another_function_returns_bytes_with_signatures():
    """
    Перевіряє, що another_function повертає байти при передачі списку підписів.
    """
    signatures = ["signature1", "signature2"]
    result = another_function(signatures)
    assert isinstance(result, (bytes, bytearray))


# Додатковий тест для DocumentGenerator, якщо модуль існує
DocumentGenerator = pytest.importorskip(
    "app.document_generator.DocumentGenerator",
    reason="DocumentGenerator не знайдено в app.document_generator",
)


def test_document_generator_render():
    """
    Перевіряє метод render у DocumentGenerator (якщо він є в проєкті).
    """
    from app.document_generator import DocumentGenerator

    template = "Hello, {name}!"
    dg = DocumentGenerator(template=template)
    output = dg.render({"name": "Alex"})
    assert isinstance(output, str)
    assert "Hello, Alex!" in output
