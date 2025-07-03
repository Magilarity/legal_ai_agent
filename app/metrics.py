# app/metrics.py
# mypy: disable-error-code="import-not-found"

from prometheus_client import CollectorRegistry, Counter, Histogram, start_http_server

# Використовуємо окремий реєстр метрик, щоб уникнути реєстрації дублікатів при повторних імпортах
registry = CollectorRegistry()

REQUEST_COUNT = Counter(
    "requests_total", "Total request count", ["endpoint"], registry=registry
)
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency", ["endpoint"], registry=registry
)


def init_metrics(port: int = 8000) -> None:
    """
    Запускає HTTP сервер для експонування метрик на вказаному порті.
    Використовує власний registry, щоб подавати лише визначені метрики.
    """
    start_http_server(port, registry=registry)
