# tests/unit/test_metrics_py.py
import socket
import threading
import time

import pytest
import requests
from prometheus_client.parser import text_string_to_metric_families

import app.metrics as metrics_mod


def test_registry_contains_metrics():
    reg = metrics_mod.registry
    # Names inside internal collector_registry
    names = list(reg._names_to_collectors.keys())
    assert "requests_total" in names
    assert "request_latency_seconds" in names


def test_request_count_increment():
    reg = metrics_mod.registry
    counter = metrics_mod.REQUEST_COUNT.labels(endpoint="test")
    initial = counter._value.get()
    counter.inc()
    assert counter._value.get() == pytest.approx(initial + 1)


def test_request_latency_observe():
    reg = metrics_mod.registry
    hist = metrics_mod.REQUEST_LATENCY.labels(endpoint="test")
    hist.observe(0.123)
    # Generate metrics text
    from prometheus_client import generate_latest

    text = generate_latest(reg).decode("utf-8")
    # Check sum and bucket entries
    assert "request_latency_seconds_sum" in text
    assert "0.123" in text


def test_init_metrics_http_server(tmp_path):
    # Find a free port
    sock = socket.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()

    # Start metrics HTTP server
    metrics_mod.init_metrics(port=port)
    time.sleep(0.1)

    resp = requests.get(f"http://127.0.0.1:{port}/metrics")
    assert resp.status_code == 200
    body = resp.text
    assert "requests_total" in body
    assert "request_latency_seconds" in body
