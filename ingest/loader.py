# ingest/loader.py
# mypy: disable-error-code="import-untyped"
import openpyxl
import requests
from typing import Any, Optional, List, Dict

# Базовий URL для API (замініть на свій)
API_BASE = "https://api.example.com"


def download_documents_with_progress(
    tender_id: str, progress_bar: Optional[Any], logger: Optional[Any]
) -> int:
    # Завантаження документів з відображенням прогресу (умовно)
    return 0


def download_documents(tender_id: str, error: bool = False) -> Optional[str]:
    # Просте завантаження документів (умовно)

    if error:
        return None
    return "downloads/123"


def process_sheet(ws: Optional[Any]) -> None:
    assert ws is not None
    ws.title  # безпечне використання, якщо ws не None
    ws.append([])


def load_documents(
    endpoint: str,
    page: int = 1,
    limit: int = 100,
    **params: Any,
) -> List[Dict]:
    """
    Завантажує всі записи з REST API з підтримкою пагінації.

    :param endpoint: відносний шлях ресурсу
    :param page: початкова сторінка (1-indexed)
    :param limit: кількість записів на сторінку
    :param params: інші GET-параметри
    :return: список словників з полем "data" згідно API
    """
    all_data: List[Dict] = []
    current = page

    while True:
        payload = {**params, "page": current, "limit": limit}
        resp = requests.get(f"{API_BASE}/{endpoint}", params=payload, timeout=10)
        if resp.status_code != 200:
            resp.raise_for_status()

        body = resp.json()
        data = body.get("data")
        if not isinstance(data, list):
            raise TypeError(f"Invalid data type: {type(data)}")

        all_data.extend(data)
        more = body.get("next_page", False)
        if not more:
            break
        current += 1

    return all_data
