from typing import Any, List, Optional


def build_report(signatures: Optional[List[Any]] = None) -> bytes:
    """
    Формує PDF-звіт на основі переданих підписів.

    :param signatures: список підписів будь-якого типу
    :return: PDF у вигляді байтів
    """
    if signatures is None:
        signatures = []
    # TODO: Реальна логіка формування PDF-стрічки
    return b""


def another_function(signatures: Optional[List[Any]] = None) -> bytes:
    """
    Додаткова умовна функція, що теж повертає PDF-байти.

    :param signatures: список підписів будь-якого типу
    :return: PDF у вигляді байтів
    """
    if signatures is None:
        signatures = []
    # TODO: Додаткова логіка обробки підписів
    return b""
