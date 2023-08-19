from sqlalchemy.orm import Session
from app.models.models import Competition, User
from app.schemas.schema import CompetitionSchema, UserSchema


def get_all_competition(db:Session, skip:int = 0, limit:int = 100):
    return db.query(Competition).offset(skip).limit(limit).all()


def create_competition(db:Session, user_id: int, competition:CompetitionSchema):
    new_competition = Competition(id=competition.id, user_id=user_id, name=competition.name)
    db.add(new_competition)
    db.commit()
    db.refresh(new_competition)
    return new_competition


def get_competition_by_id(db:Session, competition_id:int):
    return db.query(Competition).filter(Competition.id == competition_id).first()
    

def update_competiton(db:Session, competition:CompetitionSchema, user_id:int, comp_name:str):
    comp = get_competition_by_id(db,competition.id)
    comp.id = comp.id
    comp.name = comp_name
    comp.user_id = user_id
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


def delete_competition(db:Session, competition_id:int):
    com = get_competition_by_id(db,competition_id)
    db.delete(com)
    db.commit()
   
