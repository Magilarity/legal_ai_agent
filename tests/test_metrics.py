# tests/test_metrics.py

from app.metrics import registry


def test_metric_names():
    """
    Перевіряє, що в реєстрі метрик присутні основні метрики:
    - лічильник загальної кількості запитів requests_total
    - гістограма латентності запитів request_latency_seconds
    """
    # Отримуємо всі імена метрик із внутрішнього словника реєстру
    names = set(registry._names_to_collectors.keys())

    # Перевіряємо наявність ключових метрик
    assert "requests_total" in names
    assert "request_latency_seconds" in names
