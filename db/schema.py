import os

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Шлях до бази даних
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "legal_agent.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)

Base = declarative_base()
Session = sessionmaker(bind=ENGINE)


# --- Таблиця документів (тендери + нормативка) ---
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    tender = Column(String, index=True)  # номер тендеру або "normative_docs"
    title = Column(String)
    content = Column(Text)


# FTS5 для таблиці documents
FTS_DOCS = """
CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
USING fts5(title, content, content='documents', content_rowid='id');
"""


# --- Таблиця нормативних актів ---
class LegalAct(Base):
    __tablename__ = "legal_acts"
    id = Column(Integer, primary_key=True)
    act_id = Column(String, unique=True, index=True)  # внутрішній ідентифікатор акту
    title = Column(String)  # назва акту
    published = Column(DateTime)  # дата публікації
    source = Column(String)  # джерело, напр. "rada.gov.ua"
    content = Column(Text)  # повний текст


# FTS5 для legal_acts
FTS_ACTS = """
CREATE VIRTUAL TABLE IF NOT EXISTS legal_acts_fts
USING fts5(title, content, content='legal_acts', content_rowid='id');
"""


# --- Таблиця рішень (АМКУ та суди) ---
class Decision(Base):
    __tablename__ = "decisions"
    id = Column(Integer, primary_key=True)
    decision_id = Column(String, unique=True, index=True)  # внутрішній номер рішення
    source = Column(String)  # джерело, напр. "amcu.gov.ua"
    date = Column(DateTime)  # дата рішення
    pdf_path = Column(String)  # шлях до PDF у файловій системі
    meta_data = Column(Text)  # JSON-метадані (структура, учасники тощо)
    content = Column(Text)  # витягнутий текст


# FTS5 для decisions (індексуємо метадані та текст)
FTS_DECISIONS = """
CREATE VIRTUAL TABLE IF NOT EXISTS decisions_fts
USING fts5(meta_data, content, content='decisions', content_rowid='id');
"""


# --- Таблиця консультацій (портал "Радник") ---
class Consultation(Base):
    __tablename__ = "consultations"
    id = Column(Integer, primary_key=True)
    consult_id = Column(String, unique=True, index=True)  # ID консультації
    question = Column(Text)  # текст запиту
    answer = Column(Text)  # текст відповіді
    consulted_at = Column(DateTime)  # дата консультації
    source_url = Column(String)  # URL оригіналу


# FTS5 для consultations
FTS_CONSULTATIONS = """
CREATE VIRTUAL TABLE IF NOT EXISTS consultations_fts
USING fts5(question, answer, content='consultations', content_rowid='id');
"""


@event.listens_for(Base.metadata, "after_create")
def create_fts(target, connection, **kw):
    # Створюємо всі віртуальні таблиці FTS5
    for stmt in (FTS_DOCS, FTS_ACTS, FTS_DECISIONS, FTS_CONSULTATIONS):
        connection.exec_driver_sql(stmt)
