from datetime import date
from sqlalchemy.orm import Session
from src.config import SessionLocal
from src.models.competition import Competition
from src.models.user import User
from src.models.entry import Entry
from src.schemas.user import UserCreateSchema, UserSchema, UserWithEntry

from sqlalchemy.orm.collections import InstrumentedList

#Get all user data
def get_all_user(db:Session, skip:int=0, limit:int=100):
    users = db.query(User).offset(skip).limit(limit).all()
    total_user = db.query(User).count()
    return {"users":users, "total_user":total_user}


#Create new user
def create_new_user(db:Session, user:UserCreateSchema):
    db_user = User(**user.model_dump())
    # new_user = User(name = user.name, age = user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#Get user by id
def get_user_by_id(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()


#Update user
def update_user(id:int, db: Session, auth_id:int, name:str, age:int, gender:str, date_of_birth:date, is_active:bool):
    user_new = get_user_by_id(db,id)
    user_new.auth_id = auth_id
    user_new.name = name
    user_new.age = age
    user_new.gender = gender
    user_new.age = age
    user_new.date_of_birth = date_of_birth
    user_new.is_active = is_active

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


#get user with competition
def user_with_competition(id:int, db:Session):
    user = db.query(User).filter_by(id=id).first()


    if user:
        competition_list = []
        c_list = []
        for entry in user.entries:
            blank_dict = {}
            competition_list.append(entry.competition.name)
            blank_dict['name'] = entry.competition.name

            if not any(competition_name['name'] == entry.competition.name for competition_name in c_list):
                c_list.append(blank_dict)
    
        userResponce = UserWithEntry(
            id = user.id,
            name = user.name,
            # competition = user.entries  
            # competition = competition_list  
            competition = c_list  
        )
        return userResponce

    
