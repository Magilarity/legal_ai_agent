# db/schema.py

import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

# читаємо .env
load_dotenv()

Base: DeclarativeMeta = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    content = Column(String)


class LegalAct(Base):
    __tablename__ = "legal_acts"
    id      = Column(Integer, primary_key=True)
    title   = Column(String, nullable=False)
    content = Column(String)


class Consultation(Base):
    __tablename__ = "consultations"
    id      = Column(Integer, primary_key=True)
    title   = Column(String, nullable=False)
    content = Column(String)


class Decision(Base):
    __tablename__ = "decisions"
    id      = Column(Integer, primary_key=True)
    title   = Column(String, nullable=False)
    content = Column(String)


# читаємо URL
raw_url = os.getenv("DATABASE_URL", "").strip()
DATABASE_URL = raw_url if raw_url else "sqlite:///local.db"

# спочатку пробуємо підключитися до PostgreSQL
try:
    engine = create_engine(DATABASE_URL, echo=False)
    # тестове підключення
    with engine.connect():
        pass
except OperationalError:
    # якщо не вдається — падаємо на SQLite
    print(f"⚠️ Не можу підключитися до {DATABASE_URL}, використовую SQLite fallback.")
    DATABASE_URL = "sqlite:///local.db"
    engine = create_engine(DATABASE_URL, echo=False)

# фабрика сесій
Session = sessionmaker(bind=engine)