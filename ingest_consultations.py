import json
import os
from datetime import datetime
from pathlib import Path

from db.schema import Consultation, Session


def ingest_consultations(raw_folder="raw_docs/consultations"):
    session = Session()
    for file in Path(raw_folder).glob("*.json"):
        data = json.load(open(file, encoding="utf-8"))
        rec = Consultation(
            consult_id=data["id"],
            question=data["question"],
            answer=data["answer"],
            consulted_at=datetime.fromisoformat(data["date"]),
            source_url=data.get("url", ""),
        )
        session.merge(rec)
    session.commit()
    print("✅ Consultations ingested.")


if __name__ == "__main__":
    ingest_consultations()
