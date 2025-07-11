from db.schema import Session, Document
from typing import List, Dict


def ingest_tenders(tenders_data: List[Dict]) -> None:
    """
    Зберігає список тендерів у базу.
    :param tenders_data: список словників з полями для Document
    """
    with Session() as session:
        for tender_dict in tenders_data:
            doc = Document(**tender_dict)
            session.add(doc)
        session.commit()
