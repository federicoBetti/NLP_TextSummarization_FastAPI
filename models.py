from sqlalchemy import Column, Integer, String

from database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    summary = Column(String, index=True)
