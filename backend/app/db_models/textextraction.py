from sqlalchemy import Column, DateTime, Integer, String
from ..db.base_class import Base, utcnow


class TextExtraction(Base):
    # common fields
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable=False)
    # physical fields
    doc_name = Column(String)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow())

