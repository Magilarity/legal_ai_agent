import json
from datetime import datetime
from pathlib import Path

from db.schema import LegalAct, Session


def ingest_acts(raw_folder="raw_docs/acts"):
    session = Session()
    for file in Path(raw_folder).glob("*.json"):
        data = json.load(open(file, encoding="utf-8"))
        act = LegalAct(
            act_id=data["id"],
            title=data["title"],
            published=datetime.fromisoformat(data["date"]),
            source="rada.gov.ua",
            content=data.get("full_text", ""),
        )
        session.merge(act)
    session.commit()
    print("✅ Acts ingested.")


if __name__ == "__main__":
    ingest_acts()
