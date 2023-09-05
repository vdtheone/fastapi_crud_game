from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.config import Base


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Establishing the relationship with Entry
    entries = relationship("Entry", back_populates="competition")
