import os
import json
from pathlib import Path
from datetime import datetime

from db.schema import Session, LegalAct

def ingest_acts(raw_folder="raw_docs/acts"):
    session = Session()
    for file in Path(raw_folder).glob("*.json"):
        data = json.load(open(file, encoding="utf-8"))
        act = LegalAct(
            act_id    = data["id"],
            title     = data["title"],
            published = datetime.fromisoformat(data["date"]),
            source    = "rada.gov.ua",
            content   = data.get("full_text","")
        )
        session.merge(act)  # merge щоб оновлювати при повторному запуску
    session.commit()
    print("✅ Acts ingested.")

if __name__ == "__main__":
    ingest_acts()