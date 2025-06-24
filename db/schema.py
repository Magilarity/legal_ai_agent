# mypy: disable-error-code="valid-type,misc"
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    content = Column(String)

# Заглушки для типізації
ENGINE: object
Session: object
Consultation: object
Decision: object
LegalAct: object