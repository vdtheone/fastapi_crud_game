from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from src.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


