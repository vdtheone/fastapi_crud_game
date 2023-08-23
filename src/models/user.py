from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String

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
    


