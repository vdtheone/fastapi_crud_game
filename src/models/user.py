from sqlalchemy import Column, Date, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from src.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    auth_id = Column(Integer, ForeignKey("auths.id"))
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    date_of_birth = Column(Date)

    # Establishing the relationship with Auth
    auth = relationship("Auth", back_populates="user")

    # Establishing the relationship with Entry
    entries = relationship("Entry", back_populates="user")
