from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schema import UserSchema



#get all user data
def get_all_user(db:Session, skip:int=0, limit:int=100):
    return db.query(User).offset(skip).limit(limit).all()


#Create new user
def create_new_user(db:Session, user:UserSchema):
    new_user = User(id = user.id, name = user.name, age = user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

