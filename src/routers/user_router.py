from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.config import SessionLocal
from src.models.user import User
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserWithEntry
from src.services.user_crud import (
    create_new_user,
    delete_all_user,
    delete_user,
    get_all_user,
    get_user_by_id,
    update_user,
    user_with_competition,
)

user_router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get("/users/")
async def get_users(request: Request, db: Session = Depends(get_db)):
    all_user = get_all_user(request, db, 0, 100)
    return all_user


@user_router.post("/create/")
async def create_user(
    request: Request, user: UserCreateSchema, db: Session = Depends(get_db)
):
    new_user = create_new_user(request, db, user)
    return {"user": new_user}


@user_router.get("/user/{id}")
async def user_by_id(request: Request, id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(request, db, id)
    return user


@user_router.put("/update/{id}")
async def updat_user(
    request: Request, id: int, user: UserUpdateSchema, db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.id == id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="Entry not found")
    else:
        updated_user = update_user(request, id, db, user)
        return updated_user


@user_router.delete("/delete/{id}")
async def delete_user_(request: Request, id: int, db: Session = Depends(get_db)):
    deleted_message = delete_user(request, id, db)
    return deleted_message


@user_router.delete("/delete_all/")
async def delete_all(request: Request, db: Session = Depends(get_db)):
    deleted_message = delete_all_user(request, db)
    print(deleted_message)
    return deleted_message


@user_router.get("/user_competitoin/{id}/", response_model=UserWithEntry)
async def user_by_id_competition(
    request: Request, id: int, db: Session = Depends(get_db)
):
    user = user_with_competition(request, id, db)
    return user


# @user_router.get("/login", response_class=HTMLResponse)
# def registration_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})
