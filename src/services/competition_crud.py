from sqlalchemy.orm import Session, joinedload
from src.models.competition import Competition
from src.models.user import User
from src.schemas.competition import CompetitionCreateSchema, CompetitionResponse, CompetitionUpdateSchema


def get_all_competition(db:Session, skip:int = 0, limit:int = 100):
    return db.query(Competition).offset(skip).limit(limit).all()


def create_competition(db:Session, competition:CompetitionCreateSchema):
    new_competition = Competition(name=competition.name)
    db.add(new_competition)
    db.commit()
    db.refresh(new_competition)
    return new_competition


def get_competition_by_id(db:Session, competition_id:int):
    return db.query(Competition).filter(Competition.id == competition_id).first()
    

def update_competiton(db:Session, competition:CompetitionUpdateSchema, id:int):
    comp = get_competition_by_id(db,id)
    if comp:
        comp.id = comp.id
        comp.name = competition.name
        db.add(comp)
        db.commit()
        db.refresh(comp)
        return {"updated_competition":comp, "message":"Competition is updated"}
    else:
        return {"message":"Competition not found"}


def delete_competition(db:Session, competition_id:int):
    com = get_competition_by_id(db,competition_id)
    if com:
        db.delete(com)
        db.commit()
        return "competition deleted"
    else:
        return "competition not found"
    
   

def delete_all_competition(db:Session):
    db.query(Competition).delete()
    db.commit()


def get_competiton_with_entry(id:int, db:Session):
    competition = db.query(Competition).filter_by(id=id).first()
    if not competition:
        return {"message": "Competition not found"}

    competition_response = CompetitionResponse(
        name=competition.name,
        id=competition.id,
        entries=competition.entries
    )
    return competition_response