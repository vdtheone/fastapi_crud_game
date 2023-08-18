from sqlalchemy import Column, ForeignKey, Integer, String
from config import Base
from sqlalchemy.orm import relationship



# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)
    


# class Competition(Base):
#     __tablename__ = "competitions"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     name = Column(String)

#     user = relationship("User")


# class Entry(Base):
#     __tablename__ = "entries"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     competition_id = Column(Integer, ForeignKey("competitions.id"))

#     user = relationship("User")
#     competition = relationship("Competition")




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    # Define one-to-many relationship from User to Competition
    competitions = relationship("Competition", back_populates="user")


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key reference
    name = Column(String)

    # Define many-to-one relationship from Competition to User
    user = relationship("User", back_populates="competitions")
    # Define one-to-many relationship from Competition to Entry
    entries = relationship("Entry", back_populates="competition")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key reference
    competition_id = Column(Integer, ForeignKey("competitions.id"))  # Foreign key reference

    # Define many-to-one relationship from Entry to User
    user = relationship("User", back_populates="entries")
    # Define many-to-one relationship from Entry to Competition
    competition = relationship("Competition", back_populates="entries")

    
