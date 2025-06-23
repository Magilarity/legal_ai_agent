import os
from datetime import datetime
from pathlib import Path

import fitz  # для витягу тексту PDF

from db.schema import Decision, Session


def extract_pdf_text(path):
    text, doc = [], fitz.open(path)
    for p in doc:
        text.append(p.get_text())
    return "\n".join(text)


def ingest_decisions(raw_folder="raw_docs/decisions"):
    session = Session()
    for pdf in Path(raw_folder).rglob("*.pdf"):
        # полуками в назві файлу маємо decision_id та source
        # наприклад "amcu_12345.pdf"
        parts = pdf.stem.split("_", 1)
        source, decision_id = parts if len(parts) == 2 else ("unknown", pdf.stem)
        rec = Decision(
            decision_id=decision_id,
            source=source,
            date=datetime.fromtimestamp(pdf.stat().st_mtime),
            pdf_path=str(pdf),
            metadata="",  # тут можна прочитати JSON поруч, якщо є
            content=extract_pdf_text(str(pdf)),
        )
        session.merge(rec)
    session.commit()
    print("✅ Decisions ingested.")


if __name__ == "__main__":
    ingest_decisions()
