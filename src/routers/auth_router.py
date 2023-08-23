from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.auth_crud import registration
from src.config import SessionLocal
from src.schemas.auth import AuthSchema

auth_router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

@auth_router.post('/register')
async def register_user(auth:AuthSchema, db:Session = Depends(get_db)):
    new_auth_data = registration(auth,db)
    return {"auth":new_auth_data, "message":"new user created"}