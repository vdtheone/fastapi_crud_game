from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.config import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key reference
    competition_id = Column(
        Integer, ForeignKey("competitions.id")
    )  # Foreign key reference

    # Establishing the relationship with User
    user = relationship("User", back_populates="entries")

    # Establishing the relationship with Competition
    competition = relationship("Competition", back_populates="entries")
