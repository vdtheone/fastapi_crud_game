import os
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from jose import jwt
from src.models.auth import Auth
from src.models.user import User
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserWithEntry
from src.utils.return_jwt_token import access_token_required


SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


# Get all user data
@access_token_required
def get_all_user(request: Request, db: Session, skip: int = 0, limit: int = 100):
    users = db.query(User).offset(skip).limit(limit).all()
    total_user = db.query(User).count()
    return {"users": users, "total_user": total_user}


# Create new user
@access_token_required
def create_new_user(request: Request, db: Session, user: UserCreateSchema):
    access_token = request.headers.get("Authorization")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    auth = db.query(Auth).filter_by(id=payload.get("id")).first()
    user_available = db.query(User).filter_by(auth_id=auth.id).first()
    if not user_available:
        db_user = User(
            auth_id=auth.id,
            name=user.name,
            age=user.age,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return "User already created"


# Get user by id
@access_token_required
def get_user_by_id(request: Request, db: Session, user_id: int):
    access_token = request.headers.get("Authorization")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    user = (
        db.query(User)
        .filter(User.id == user_id, User.auth_id == payload.get("id"))
        .first()
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user
@access_token_required
def update_user(request: Request, id: int, db: Session, user: UserUpdateSchema):
    access_token = request.headers.get("Authorization")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    auth = db.query(Auth).filter_by(id=payload.get("id")).first()
    user_new = get_user_by_id(request, db, id)
    user_new.auth_id = auth.id
    user_new.name = user.name
    user_new.age = user.age
    user_new.gender = user.gender
    user_new.age = user.age
    user_new.date_of_birth = user.date_of_birth
    db.commit()
    db.refresh(user_new)
    return user_new


# delete user
def delete_user(request: Request, id: int, db: Session):
    user_to_delete = get_user_by_id(request, db, id)
    db.delete(user_to_delete)
    db.commit()
    return {"message": "User deleted successfully"}


# delete all user
@access_token_required
def delete_all_user(request: Request, db: Session):
    db.query(User).delete()
    db.commit()
    return {"Message": "Deleted All User Successfully"}


# get user with competition
@access_token_required
def user_with_competition(request: Request, id: int, db: Session):
    user = db.query(User).filter_by(id=id).first()
    if user:
        competition_list = []
        c_list = []
        for entry in user.entries:
            blank_dict = {}
            competition_list.append(entry.competition.name)
            blank_dict["name"] = entry.competition.name

            if not any(
                competition_name["name"] == entry.competition.name
                for competition_name in c_list
            ):
                c_list.append(blank_dict)

        userResponce = UserWithEntry(
            id=user.id,
            name=user.name,
            # competition = user.entries
            # competition = competition_list
            competition=c_list,
        )
        return userResponce
