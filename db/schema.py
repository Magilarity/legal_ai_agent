# db/schema.py

import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

# Базовий клас для всіх моделей
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


# Параметри підключення до БД
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")
engine = create_engine(DATABASE_URL, echo=False)

# Фабрика сесій
Session = sessionmaker(bind=engine)