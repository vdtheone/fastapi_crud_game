from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from src.config import Base


class Auth(Base):
    __tablename__ = "auths"

    id : int = Column(Integer, primary_key=True, index=True)
    username : str = Column(String, unique=True,index=True)
    email : str = Column(String, unique=True, index=True)
    hashed_password :str = Column(String)
    created_at : DateTime = Column(DateTime)
    updated_at : DateTime = Column(DateTime)

    