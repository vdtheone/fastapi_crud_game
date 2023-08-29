from fastapi import APIRouter, Depends, HTTPException, Request, status

from sqlalchemy.orm import Session

from src.services.auth_crud import (
    delete_auth,
    get_all,
    get_by_id,
    login_user,
    registration,
    update_auth_user,
)
from src.schemas.auth import (
    AuthCreateSchema,
    AuthLoginSchema,
    AuthSchema,
    AuthUpdateSchema,
)
from src.utils.generate_jwt_token import create_access_token_another_function
from src.config import SessionLocal
from jose import JWTError, jwt
import os


auth_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 32 bit secret key
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

# encryption algorithm
ALGORITHM = os.environ.get("ALGORITHM")


# the endpoint to get the token
@auth_router.get("/get_token")
async def get_token():
    # data to be signed using token
    data = {"username": "seema@gmail.com", "password": "seema"}
    token = create_access_token_another_function(data=data)
    return {"Authorization ": token}


# the endpoint to verify the token
@auth_router.post("/verify_token")
async def verify_token(token: str):
    try:
        # try to decode the token, it will raise error if the token is not correct
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@auth_router.post("/register")
async def register_user(auth: AuthCreateSchema, db: Session = Depends(get_db)):
    new_auth_data = registration(auth, db)
    return new_auth_data


@auth_router.post("/")
async def login(user: AuthLoginSchema, db: Session = Depends(get_db)):
    user = login_user(db, user)
    return user


@auth_router.get("/all/", response_model=list[AuthSchema])
async def get_users(request:Request, db: Session = Depends(get_db)):
    all_user = get_all(request, db, 0, 100)
    return all_user


@auth_router.get("/{id}")
async def get_auth_by_id(request:Request, id: int, db: Session = Depends(get_db)):
    user_by_id = get_by_id(request, db, id)
    return user_by_id


@auth_router.put("/update/{id}")
async def update(request:Request, id: int, auth: AuthUpdateSchema, db: Session = Depends(get_db)):
    updated_auth_user = update_auth_user(request, db, id, auth)
    return updated_auth_user


@auth_router.delete("/delete/{id}")
async def delete(request:Request, id: int, db: Session = Depends(get_db)):
    deleted = delete_auth(request, db, id)
    return deleted
