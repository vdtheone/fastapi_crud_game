import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.auth_crud import delete_auth, get_all, get_by_id, login, registration, update_auth_user
from src.config import SessionLocal
from src.schemas.auth import AuthCreateSchema, AuthLoginSchema, AuthSchema, AuthUpdateSchema

auth_router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

@auth_router.post('/register')
async def register_user(auth:AuthCreateSchema, db:Session = Depends(get_db)):
    new_auth_data = registration(auth,db)
    return {"auth":new_auth_data, "message":"new user created"}


@auth_router.post("/")
async def login_user(user : AuthLoginSchema, db:Session = Depends(get_db)):
    user = login(db,user)
    return user


@auth_router.get('/all/',response_model=list[AuthSchema])
async def get_users(db:Session=Depends(get_db)):
    all_user = get_all(db,0,100)
 
    return all_user


@auth_router.get("/{id}")
async def get_auth_by_id(id:int, db:Session = Depends(get_db)):
    user_by_id = get_by_id(db,id)
    return user_by_id

@auth_router.put("/update/{id}")
async def update(id:int, auth: AuthUpdateSchema, db:Session = Depends(get_db)):
    updated_auth_user = update_auth_user(db,id,auth)
    return updated_auth_user


@auth_router.delete("/delete/{id}")
async def delete(id:int, db:Session = Depends(get_db)):
    deleted = delete_auth(db, id)
    return deleted