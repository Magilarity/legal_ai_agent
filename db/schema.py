# db/schema.py

import os
from dotenv import load_dotenv           # <<< ДОДАЛИ
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

# Завантажуємо .env з кореня проєкту
load_dotenv()

# Базовий клас
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


# Тепер гарантовано беремо або з .env, або дефолт
raw_url = os.getenv("DATABASE_URL")
DATABASE_URL = raw_url if raw_url and raw_url.strip() else "sqlite:///local.db"

# Створюємо engine
engine = create_engine(DATABASE_URL, echo=False)

# Фабрика сесій
Session = sessionmaker(bind=engine)