import os
from hashlib import sha256

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, Request, status
from jose import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.auth import Auth
from src.schemas.auth import AuthCreateSchema, AuthLoginSchema, AuthUpdateSchema
from src.utils.generate_jwt_token import create_access_token, create_refresh_token
from src.utils.return_jwt_token import access_token_required

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def hash_password(password: str):
    hash_obj = sha256()
    hash_obj.update(password.encode("utf-8"))
    hashed_password = hash_obj.hexdigest()
    return hashed_password


def registration(auth: AuthCreateSchema, db: Session):
    try:
        email_object = validate_email(auth.email)
        correct_email = email_object.email
        new_user = Auth(
            username=auth.username,
            email=correct_email,
            hashed_password=hash_password(auth.hashed_password),
            created_at=auth.created_at,
            updated_at=auth.updated_at,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except EmailNotValidError as errorMsg:
        raise HTTPException(status_code=501, detail=str(errorMsg))

    except IntegrityError as e:
        if "ix_auths_email" in str(e).lower():
            raise HTTPException(status_code=501, detail="Email address already exists.")
        if "ix_auths_username" in str(e).lower():
            raise HTTPException(
                status_code=501, detail="Username address already exists."
            )


def login_user(db: Session, auth: AuthLoginSchema):
    try:
        hash_pass = hash_password(auth.password)
        email_object = validate_email(auth.username)
        if email_object:
            email_exist = (
                db.query(Auth)
                .filter(
                    Auth.email == email_object.email, Auth.hashed_password == hash_pass
                )
                .first()
            )

            if email_exist is None or email_exist.is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username and password",
                    headers={"WWW-Authenticate": "Basic"},
                )
            else:
                auth_dict = {"id": email_exist.id, "username": email_exist.username}
                return {
                    "access_token": create_access_token(auth_dict),
                    "refresh_token": create_refresh_token(auth_dict),
                }
    except Exception:
        user = (
            db.query(Auth)
            .filter(Auth.username == auth.username, Auth.hashed_password == hash_pass)
            .first()
        )
        if user is None or user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username and password",
                headers={"WWW-Authenticate": "Basic"},
            )
        else:
            auth_dict = {"id": user.id, "username": user.username}
            return {
                "access_token": create_access_token(auth_dict),
                "refresh_token": create_refresh_token(auth_dict),
            }


@access_token_required
def get_all(request: Request, db: Session, skip: int = 0, limit: int = 100):
    users = db.query(Auth).offset(skip).limit(limit).all()
    db.query(Auth).count()
    return users


@access_token_required
def get_by_id(request: Request, db: Session, id: int):
    access_token = request.headers.get("Authorization")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    auth_user = (
        db.query(Auth).filter(Auth.id == id, Auth.id == payload.get('id')).first()
    )
    if auth_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return auth_user


def update_auth_user(request: Request, db: Session, id: int, auth: AuthUpdateSchema):
    update_auth_user = get_by_id(request, db, id)

    update_auth_user.hashed_password = hash_password(auth.hashed_password)
    update_auth_user.updated_at = auth.updated_at

    db.commit()
    db.refresh(update_auth_user)
    return update_auth_user


def delete_auth(request: Request, db: Session, id: int):
    delete_auth_user = get_by_id(request, db, id)
    delete_auth_user.is_deleted = True
    db.commit()
    db.refresh(delete_auth_user)
    return {"message": "user deleted successfully"}
