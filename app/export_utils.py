import logging
import os

from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Логування без “детача” stdout
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Зареєструйте шрифт DejaVu Sans (підтримка кирилиці)
# Покладіть файл DejaVuSans.ttf у корінь проєкту
FONT_NAME = "DejaVuSans"
FONT_PATH = "DejaVuSans.ttf"
if not os.path.exists(FONT_PATH):
    logging.error(f"Не знайдено шрифт {FONT_PATH} — помістіть його в корінь проєкту")
else:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def save_analysis_to_docx(
    tender_id: str,
    analysis_text: str,
    signatures: list = None,
    output_dir: str = "exports",
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{tender_id}_аналіз.docx")

    doc = Document()
    doc.add_heading(f"Аналіз тендеру {tender_id}", level=0)
    for section in analysis_text.split("\n\n"):
        doc.add_paragraph(section)

    if signatures:
        doc.add_heading("Підписи з файлів .p7s", level=1)
        for sig in signatures:
            doc.add_paragraph(sig)

    try:
        doc.save(file_path)
        logging.info(f"✅ Word-звіт збережено: {file_path}")
    except Exception as e:
        logging.error(f"❌ Помилка при збереженні DOCX: {e}")
        raise
    return file_path


def save_analysis_to_pdf(
    tender_id: str,
    analysis_text: str,
    signatures: list = None,
    output_dir: str = "exports",
) -> str:
    """
    Генерує PDF-звіт з кирилицею через ReportLab.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{tender_id}_аналіз.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    if FONT_NAME not in pdfmetrics.getRegisteredFontNames():
        logging.error("Шрифт не зареєстровано — PDF може не містити кирилиці")
        font_to_use = "Helvetica"
    else:
        font_to_use = FONT_NAME

    c.setFont(font_to_use, 12)
    text = c.beginText(40, height - 40)
    text.textLine(f"Аналіз тендеру {tender_id}")
    text.textLine("")

    # Додаємо аналіз текстом
    for line in analysis_text.split("\n"):
        text.textLine(line)

    # Додаємо підписи
    if signatures:
        text.textLine("")
        text.textLine("Підписи з файлів .p7s:")
        for sig in signatures:
            text.textLine(sig)

    c.drawText(text)
    try:
        c.showPage()
        c.save()
        logging.info(f"✅ PDF-звіт збережено: {file_path}")
    except Exception as e:
        logging.error(f"❌ Помилка при збереженні PDF: {e}")
        raise

    return file_path
