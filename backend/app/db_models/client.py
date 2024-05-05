from sqlalchemy import Column, Integer, String, DateTime

from ..db.base_class import Base, utcnow


class Client(Base):
    # common fields
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # physical fields
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow())

