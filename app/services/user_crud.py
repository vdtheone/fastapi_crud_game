from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schema import UserSchema



#Get all user data
def get_all_user(db:Session, skip:int=0, limit:int=100):
    users = db.query(User).offset(skip).limit(limit).all()
    total_user = db.query(User).count()
    return {"users":users, "total_user":total_user}


#Create new user
def create_new_user(db:Session, user:UserSchema):
    new_user = User(name = user.name, age = user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#Get user by id
def get_user_by_id(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()


#Update user
def update_user(id:int, db: Session, name:str, age:int):
    user_new = get_user_by_id(db,id)
    user_new.name = name
    user_new.age = age
    db.commit()
    db.refresh(user_new)
    return user_new


#delete user
def delete_user(id:int, db:Session):
    user_new = get_user_by_id(db,id)
    db.delete(user_new)
    db.commit()


#delete all user
def delete_all_user(db:Session):
    db.query(User).delete()
    db.commit()
    
    
