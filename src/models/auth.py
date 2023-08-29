from sqlalchemy import Boolean, Column, DateTime, Integer, String
from src.config import Base
from sqlalchemy.orm import relationship


class Auth(Base):
    __tablename__ = "auths"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    email: str = Column(String, unique=True, index=True)
    hashed_password: str = Column(String)
    is_active: bool = Column(Boolean, default=True)
    created_at: DateTime = Column(DateTime)
    updated_at: DateTime = Column(DateTime)
    is_deleted: bool = Column(Boolean, default=False)

    # Establishing the relationship with User
    user = relationship("User", back_populates="auth")
