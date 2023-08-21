from fastapi import APIRouter, Depends, HTTPException
from app.config.config import SessionLocal
from app.schemas.schema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.services.user_crud import create_new_user, delete_all_user, delete_user, get_all_user, get_user_by_id, update_user
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


@user_router.post("/create/")
async def create_user(user: UserCreateSchema, db:Session = Depends(get_db)):
    new_user = create_new_user(db, user)
    return {"user":new_user,"message":"user created", }


@user_router.get("/user/{id}")
async def user_by_id(id:int, db:Session = Depends(get_db)):
    user = get_user_by_id(db,id)
    return user


@user_router.put("/update/{id}")
async def updat_user(id:int, user:UserUpdateSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="Entry not found")
    else:
        updated_user = update_user(id, db, user.name, user.age)
        return updated_user


@user_router.delete("/delete/{id}")
async def delete_user_(id:int, db:Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.id == id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="Entry not found")
    else:
        delete_user(id,db)
        return {"message":"User deleted"}
    

@user_router.delete("/delete_all/")
async def delete_all(db:Session = Depends(get_db)):
    delete_all_user(db)
    return {"message":"Delete all users"}