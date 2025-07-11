from db.schema import Session, LegalAct
from typing import List, Dict


def ingest_acts(acts_data: List[Dict]) -> None:
    """
    Зберігає список юридичних актів у базу.
    :param acts_data: список словників з полями для LegalAct
    """
    with Session() as session:
        for act_dict in acts_data:
            legal_act = LegalAct(**act_dict)
            session.add(legal_act)
        session.commit()
