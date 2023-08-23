from sqlalchemy.orm import Session
from src.schemas.auth import AuthSchema
from src.models.auth import Auth

def registration(auth:AuthSchema, db:Session):
    # new_user = Auth(name = auth.name, username = auth.username, email = auth.email, hashed_password = auth.hashed_password, gender = auth.gender, age = auth.age)  
    new_user = Auth(**auth.model_dump())
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)
    return new_user
