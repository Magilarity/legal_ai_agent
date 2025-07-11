from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, DeclarativeMeta

# Імпортуємо налаштування з app/config.py
from app.config import settings

Base: DeclarativeMeta = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    content = Column(String)


class LegalAct(Base):
    __tablename__ = "legal_acts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)


class Consultation(Base):
    __tablename__ = "consultations"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)


class Decision(Base):
    __tablename__ = "decisions"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)


# Отримуємо URL з Pydantic Settings (вже валідовано)
raw_url = settings.database_url.strip()
DATABASE_URL = raw_url if raw_url else "sqlite:///local.db"

# Першочергово намагаємося підключитися до PostgreSQL
try:
    engine = create_engine(DATABASE_URL, echo=False)
    # Тестове підключення
    with engine.connect():
        pass
except (OperationalError, ModuleNotFoundError):
    # Фолбек на SQLite
    print(f"⚠️ Не можу підключитися до {DATABASE_URL}, використовую SQLite fallback.")
    DATABASE_URL = "sqlite:///local.db"
    engine = create_engine(DATABASE_URL, echo=False)

# Alias for compatibility
ENGINE = engine

# Фабрика сесій
Session = sessionmaker(bind=engine)

# Перелік таблиць для тестування створення схеми
TABLES = [
    Document.__tablename__,
    LegalAct.__tablename__,
    Consultation.__tablename__,
    Decision.__tablename__,
]
