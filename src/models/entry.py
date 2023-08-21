from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from src.config import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key reference
    competition_id = Column(
        Integer, ForeignKey("competitions.id")
    )  # Foreign key reference

