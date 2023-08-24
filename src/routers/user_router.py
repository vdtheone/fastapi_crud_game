from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.config import SessionLocal
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserWithEntry
from src.services.user_crud import create_new_user, delete_all_user, delete_user, get_all_user, get_user_by_id, update_user, user_with_competition
from sqlalchemy.orm import Session

from src.models.user import User

user_router = APIRouter()

templates = Jinja2Templates(directory="templates")

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
    return {"user":new_user, "message":"user created"}


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
        # updated_user = update_user(id, db, user.name, user.age)
        updated_user = update_user(id, db, user.auth_id, user.name, user.age, user.gender, user.date_of_birth, user.is_active)
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


@user_router.get("/user_competitoin/{id}/", response_model=UserWithEntry)
async def user_by_id_competition(id:int, db:Session = Depends(get_db)):
    user = user_with_competition(id,db)
    return user


    


# @user_router.get("/login", response_class=HTMLResponse)
# def registration_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})