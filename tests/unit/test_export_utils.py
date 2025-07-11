import pytest

from app.export_utils import build_report, another_function


def test_build_report_returns_bytes():
    result = build_report()
    assert isinstance(result, (bytes, bytearray))


def test_build_report_with_signatures():
    sigs = [{"sig": "data"}]
    result = build_report(sigs)
    assert isinstance(result, (bytes, bytearray))


def test_another_function_defaults():
    result = another_function()
    assert isinstance(result, (bytes, bytearray))


def test_another_function_with_signatures():
    result = another_function(["sig1"])
    assert isinstance(result, (bytes, bytearray))
