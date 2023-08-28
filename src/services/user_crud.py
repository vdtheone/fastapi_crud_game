import os
from fastapi import Request
from sqlalchemy.orm import Session
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from src.models.auth import Auth
from src.models.user import User
from src.schemas.user import UserCreateSchema, UserUpdateSchema, UserWithEntry
from src.utils.return_jwt_token import return_access_token


SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


# Get all user data
def get_all_user(request: Request, db: Session, skip: int = 0, limit: int = 100):
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        payload = return_access_token(access_token)
        if dict == type(payload):
            users = db.query(User).offset(skip).limit(limit).all()
            total_user = db.query(User).count()
            return {"users": users, "total_user": total_user}
        return {"Error": payload}
    else:
        return {"Error": "Token not provided"}


# Create new user
def create_new_user(request: Request, db: Session, user: UserCreateSchema):
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        payload = return_access_token(access_token)
        if dict == type(payload):
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
                return {"message": "User is already created"}
        else:
            return {"Error": payload}
    else:
        return {"Error": "Token not provided"}


# Get user by id
def get_user_by_id(request: Request, db: Session, user_id: int):
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        payload = return_access_token(access_token)
        if dict == type(payload):
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return user
            else:
                return {"message": "user not found"}
        else:
            return {"Error": payload}
    else:
        return {"Error": "Token not provided"}


# Update user
def update_user(request: Request, id: int, db: Session, user: UserUpdateSchema):
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        payload = return_access_token(access_token)
        if dict == type(payload):
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
        else:
            return {"Error": payload}
    else:
        return {"Error": "Token not provided"}



# delete user
def delete_user(request: Request, id: int, db: Session):
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        payload = return_access_token(access_token)
        if dict == type(payload):
            user_new = get_user_by_id(request, db, id)
            db.delete(user_new)
            db.commit()
            return {"Message": "User Deleted Successfully"}
        else: 
            return {"Error": payload}
    else:
        return {"Error": "Token not provided"}
 
    


# delete all user
def delete_all_user(request: Request, db: Session):
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        payload = return_access_token(access_token)
        if access_token is not None:
            payload = return_access_token(access_token)
            if dict == type(payload):
                db.query(User).delete()
                db.commit()
                return {"Message": "Deleted All User Successfully"}
            else: 
                return {"Error": payload}
    else:
        return {"Error": "Token not provided"}



# get user with competition
def user_with_competition(request: Request, id: int, db: Session):
    access_token = request.headers.get("Authorization")
    if access_token is not None:
        payload = return_access_token(access_token)
        if dict == type(payload):
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
            else:
                return {"Error": payload}
    else:
        return {"Error": "Token not provided"}
