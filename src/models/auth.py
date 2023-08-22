from sqlalchemy import Boolean, Column, DateTime, Integer, String
from src.config import Base


class auth(Base):
    __tablename__ = "auhts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username: Column(String, unique=True,index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    gender = Column(String)
    age = Column(Integer)
    birthdate = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    