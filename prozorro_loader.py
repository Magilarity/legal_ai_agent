from typing import Optional, Any
import openpyxl
import requests

def download_documents_with_progress(tender_id: str, progress_bar: Optional[Any], logger: Optional[Any]) -> int:
    # Завантаження документів з відображенням прогресу (умовно)
    return 0

def download_documents(tender_id: str) -> Optional[str]:
    # Просте завантаження документів (умовно)
    error = False
    if error:
        return None
    return "downloads/123"

def process_sheet(ws: Optional[Any]) -> None:
    assert ws is not None
    ws.title  # безпечне використання, якщо ws не None
    ws.append([])