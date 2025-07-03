# app/document_loader.py
from collections import namedtuple
from typing import List


def load(path: str) -> str:
    """
    Читає файл за вказаним шляхом і повертає вміст як строку.
    Спробує декодувати спочатку в utf-8, якщо не вдасться — у cp1251.
    """
    try:
        with open(path, "rb") as f:
            data = f.read()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("cp1251", errors="ignore")
        return text
    except Exception:
        return ""


def extract_text_from_file(path: str) -> str:
    """
    Із файлу за шляхом витягує текст.
    """
    return load(path)


class DocumentLoader:
    """
    Обгортка для завантаження документів: читає файл, перевіряє непорожнечу
    та повертає список об'єктів з атрибутом page_content.
    """

    def load(self, path: str) -> List:
        """
        Завантажує текст з файлу та повертає список документів.
        """
        text = extract_text_from_file(path)
        if not text or not text.strip():
            raise ValueError(f"Empty document or no text extracted: {path}")
        Doc = namedtuple("Doc", ["page_content"])
        return [Doc(page_content=text)]
