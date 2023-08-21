from sqlalchemy.orm import Session
from src.models.competition import Competition
from src.models.user import User
from src.schemas.competition import CompetitionCreateSchema, CompetitionUpdateSchema


def get_all_competition(db:Session, skip:int = 0, limit:int = 100):
    return db.query(Competition).offset(skip).limit(limit).all()


def create_competition(db:Session, competition:CompetitionCreateSchema):
    new_competition = Competition(user_id=competition.user_id, name=competition.name)
    db.add(new_competition)
    db.commit()
    db.refresh(new_competition)
    return new_competition


def get_competition_by_id(db:Session, competition_id:int):
    return db.query(Competition).filter(Competition.id == competition_id).first()
    

def update_competiton(db:Session, competition:CompetitionUpdateSchema, id:int):
    comp = get_competition_by_id(db,id)
    comp.id = comp.id
    comp.name = competition.name
    comp.user_id = competition.user_id
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


def delete_competition(db:Session, competition_id:int):
    com = get_competition_by_id(db,competition_id)
    db.delete(com)
    db.commit()
    
   

def delete_all_competition(db:Session):
    db.query(Competition).delete()
    db.commit()