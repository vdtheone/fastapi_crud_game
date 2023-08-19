from fastapi import APIRouter, Depends
from app.config.config import SessionLocal
from app.schemas.schema import UserSchema
from app.services.user_crud import create_new_user, delete_user, get_all_user, get_user_by_id, update_user
from sqlalchemy.orm import Session

from app.models.models import User

user_router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

@user_router.get('/users/')
async def get_users(db:Session=Depends(get_db)):
    all_user = get_all_user(db,0,100)
    return all_user


@user_router.post("/create")
async def create_user(request: UserSchema, db:Session = Depends(get_db)):
    new_user = create_new_user(db, request)
    return {"message":"user created", "user":new_user}


@user_router.get("/user/{id}")
async def user_by_id(id:int, db:Session = Depends(get_db)):
    user = get_user_by_id(db,id)
    return user


@user_router.put("/update/{id}")
async def updat_user(id:int, user:UserSchema, db: Session = Depends(get_db)):
    updated_user = update_user(user.id, db, user.name, user.age)
    return updated_user


@user_router.delete("/delete/{id}")
async def delete_user_(id:int, db:Session = Depends(get_db)):
    delete_user(id,db)
    return {"message":"User deleted"}

