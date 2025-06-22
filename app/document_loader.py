import os
import logging
import fitz  # PyMuPDF
from docx import Document as DocxDocument
from striprtf.striprtf import rtf_to_text
from PIL import Image
import pytesseract

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_file(path: str) -> str:
    """
    Витягує текст з файлу за його шляхом.
    Підтримує PDF, DOCX, RTF, TXT і зображення (OCR).
    """
    ext = os.path.splitext(path)[1].lower()

    try:
        if ext == ".pdf":
            doc = fitz.open(path)
            pages = [page.get_text() for page in doc]
            return "\n".join(pages)

        elif ext == ".docx":
            doc = DocxDocument(path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext == ".rtf":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                rtf = f.read()
            return rtf_to_text(rtf)

        elif ext == ".txt":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"]:
            img = Image.open(path)
            # вказуємо українську та англійську для кращого розпізнавання
            return pytesseract.image_to_string(img, lang="ukr+eng")

        else:
            logger.warning(f"Непідтримуваний формат файлу: {path}")
            return ""

    except Exception as e:
        logger.error(f"Помилка читання {ext.upper()} {path}: {e}")
        return ""