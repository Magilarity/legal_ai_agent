import io
import logging
import sys

from docx import Document

# Забезпечити правильне виведення у консоль з UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

logging.basicConfig(level=logging.INFO)


def generate_docx_from_template(template_path, context, output_path):
    try:
        doc = Document(template_path)
        for paragraph in doc.paragraphs:
            for key, value in context.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(
                        f"{{{{{key}}}}}", str(value)
                    )
        doc.save(output_path)
        logging.info(f"Документ збережено: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Помилка при створенні документа: {e}")
        raise
