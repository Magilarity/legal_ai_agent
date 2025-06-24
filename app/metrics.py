# mypy: disable-error-code="import-not-found"
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter(
    "requests_total",
    "Total request count",
    ["endpoint"],
)
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency",
    ["endpoint"],
)


def init_metrics(port: int = 8000) -> None:
    # Запуск сервера для експонування метрик
    start_http_server(port)