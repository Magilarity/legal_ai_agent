# ingest/tenders.py

from db.schema import engine, Document, Session


def extract_text(path: str) -> str:
    # Реалізація отримання тексту з файлу (поки заглушка)
    return ""


def ingest_all(downloads_folder: str = "downloads") -> None:
    # Реалізація пакетного завантаження/обробки (поки заглушка)
    pass


def load_tenders() -> list[Document]:
    """
    Завантажує всі тендери (документи) з бази даних.
    """
    session = Session()
    try:
        return session.query(Document).all()
    finally:
        session.close()
