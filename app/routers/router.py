from fastapi import APIRouter, Depends
from app.config.config import SessionLocal
from app.schemas.schema import UserSchema
from app.services.user_crud import create_new_user, get_all_user
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

@router.get('/users/')
async def get_users(db:Session=Depends(get_db)):
    all_user = get_all_user(db,0,100)
    return all_user


@router.post("/create")
async def create_user(request: UserSchema, db:Session = Depends(get_db)):
    new_user = create_new_user(db, request)
    return {"message":"user created", "user":new_user}
