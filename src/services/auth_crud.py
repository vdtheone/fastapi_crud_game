from sqlalchemy.orm import Session
from src.schemas.auth import AuthCreateSchema, AuthLoginSchema, AuthSchema, AuthUpdateSchema
from src.models.auth import Auth
from hashlib import sha256


def hash_password(password:str):
    hash_obj = sha256()
    hash_obj.update(password.encode('utf-8'))
    hashed_password = hash_obj.hexdigest()
    return hashed_password



def registration(auth: AuthCreateSchema, db: Session):
    new_user = Auth(
        username = auth.username, 
        email = auth.email, 
        hashed_password = hash_password(auth.hashed_password),
        created_at = auth.created_at, 
        updated_at = auth.updated_at
    )
    # new_user = Auth(**auth.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login(db:Session, auth:AuthLoginSchema):
    hash_pass = hash_password(auth.password)
    user = db.query(Auth).filter(Auth.username == auth.username, Auth.hashed_password == hash_pass).first()
    if user is None:
        return {"message":"Username and password are wrong"}
    else:
        return user


def get_all(db:Session, skip:int=0, limit:int=100):
    users = db.query(Auth).offset(skip).limit(limit).all()
    total_user = db.query(Auth).count()
    return users


def get_by_id(db:Session, id:int):
    return db.query(Auth).filter(Auth.id == id).first()


def update_auth_user(db:Session, id:int, auth:AuthUpdateSchema):
    update_auth_user = get_by_id(db,id)
    
    if update_auth_user:
        for key,value in auth.model_dump().items():
            if key=="hashed_password" and value is not None:
                hash = hash_password(value)
                setattr(update_auth_user, key,hash)
            else:
                setattr(update_auth_user, key, value)
        
        db.commit()
        db.refresh(update_auth_user)
        return update_auth_user


def delete_auth(db:Session, id:int):
    delete_auth_user = get_by_id(db,id)
    db.delete(delete_auth_user)
    db.commit()
    return {"message":"user deleted successfully"}
    

