# tests/unit/test_logging_config.py
import logging
import re
import pytest
from logging.handlers import SMTPHandler, RotatingFileHandler

import app.logging_config as log_mod

# Dynamically locate the logging configuration function (e.g., setup_logging)
setup_func = None
for attr in dir(log_mod):
    if attr.lower().startswith(("setup", "configure")):
        fn = getattr(log_mod, attr)
        if callable(fn):
            setup_func = fn
            break

if setup_func is None:
    pytest.skip(
        "No setup/configure function found in app.logging_config",
        allow_module_level=True,
    )


@pytest.mark.parametrize(
    "handler_types",
    [
        None,
        [],
        ["SMTPHandler"],
        ["RotatingFileHandler", "StreamHandler"],
    ],
)
def test_handler_types_registration(tmp_path, monkeypatch, handler_types):
    """
    Tests that setup_func registers the correct handlers based on handler_types.
    If handler_types is None or empty, default handlers (File+Stream) are used.
    """
    # Prepare a temporary log directory
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    # Clear existing handlers
    logger = logging.getLogger()
    logger.handlers.clear()

    # Call setup
    if handler_types is None:
        setup_func(level="INFO")
    else:
        setup_func(level="INFO", handler_types=handler_types)

    names = [type(h).__name__ for h in logger.handlers]

    if handler_types is None or not handler_types:
        # Expect at least FileHandler (or RotatingFileHandler) and StreamHandler
        assert any(
            n in ("FileHandler", "RotatingFileHandler") for n in names
        ), f"Expected file handler in {names}"
        assert "StreamHandler" in names, f"Expected StreamHandler in {names}"
    else:
        for req in handler_types:
            assert req in names, f"Expected {req} in {names}"


def test_log_message_format_and_level(tmp_path, monkeypatch, caplog):
    """
    Tests that log messages include ISO-like timestamp, log level, and message text.
    """
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    logger = logging.getLogger()
    logger.handlers.clear()

    # Configure at DEBUG
    setup_func(level="DEBUG")
    caplog.set_level(logging.DEBUG)

    # Emit a log
    logger.debug("AdvancedTest message format")

    # Capture output lines
    lines = caplog.text.strip().splitlines()
    assert lines, "No log output captured"
    last = lines[-1]

    # Regex: YYYY-MM-DDThh:mm:ss ... DEBUG ... message
    pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*DEBUG.*AdvancedTest message format"
    assert re.search(pattern, last), f"Log format mismatch: {last}"


def test_email_handler_configuration(tmp_path, monkeypatch):
    """
    If SMTPHandler is included, ensure it's configured with env variables.
    """
    # Set environment for SMTP
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_USER", "user@example.com")
    monkeypatch.setenv("SMTP_PASS", "secret")
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")

    logger = logging.getLogger()
    logger.handlers.clear()

    # Include SMTPHandler explicitly
    setup_func(level="ERROR", handler_types=["SMTPHandler"])

    # Find SMTPHandler
    handlers = logger.handlers
    smtp = [h for h in handlers if isinstance(h, SMTPHandler)]
    assert smtp, "SMTPHandler not registered"
    smtp_h = smtp[0]

    # Verify its attributes
    assert smtp_h.mailhost == ("smtp.example.com", 587)
    assert smtp_h.fromaddr == "user@example.com"
    assert smtp_h.toaddrs == ["admin@example.com"]
    assert smtp_h.credentials == ("user@example.com", "secret")
