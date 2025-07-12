# app/metrics.py
# mypy: disable-error-code="import-not-found"

import errno

from prometheus_client import CollectorRegistry, Counter, Histogram, start_http_server

# Використовуємо окремий реєстр метрик, щоб уникнути реєстрації дублікатів при повторних імпортах
registry = CollectorRegistry()

# Лічильник загальної кількості запитів, з міткою endpoint
REQUEST_COUNT = Counter(
    "requests_total", "Загальна кількість запитів", ["endpoint"], registry=registry
)

# Гістограма латентності запитів, з міткою endpoint
REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Час обробки запиту в секундах",
    ["endpoint"],
    registry=registry,
)


def init_metrics(port: int = 8001) -> None:
    """
    Запускає HTTP-сервер Prometheus на вказаному порту для експонування метрик.
    Ігнорує помилку, якщо порт вже зайнятий.
    """
    try:
        start_http_server(port, registry=registry)
    except OSError as e:
        # EADDRINUSE: порт вже використовується – просто продовжуємо
        if e.errno == errno.EADDRINUSE:
            pass
        else:
            raise
