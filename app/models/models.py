from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from app.config.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key reference
    name = Column(String)


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key reference
    competition_id = Column(
        Integer, ForeignKey("competitions.id")
    )  # Foreign key reference

