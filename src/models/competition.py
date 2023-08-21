from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from src.config import Base


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key reference
    name = Column(String)
