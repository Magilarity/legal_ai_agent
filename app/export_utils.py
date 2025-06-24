from typing import Any, List, Optional
import docx
from reportlab.lib.pagesizes import A4


def build_report(signatures: Optional[List[Any]] = None) -> bytes:
    if signatures is None:
        signatures = []
    # Формування PDF (умовно)
    return b""


def another_function(signatures: Optional[List[Any]] = None) -> bytes:
    if signatures is None:
        signatures = []
    # Додаткова логіка (умовно)
    return b""
