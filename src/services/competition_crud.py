from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from src.models.competition import Competition
from src.schemas.competition import (
    CompetitionCreateSchema,
    CompetitionResponse,
    CompetitionUpdateSchema,
)
from src.utils.return_jwt_token import access_token_required


@access_token_required
def get_all_competition(request: Request, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Competition).offset(skip).limit(limit).all()


@access_token_required
def create_competition(
    request: Request, db: Session, competition: CompetitionCreateSchema
):
    new_competition = Competition(name=competition.name)
    db.add(new_competition)
    db.commit()
    db.refresh(new_competition)
    return new_competition


@access_token_required
def get_competition_by_id(request: Request, db: Session, competition_id: int):
    competition = db.query(Competition).filter(Competition.id == competition_id).first()
    if competition is None:
        raise HTTPException(status_code=404, detail="competition not found")
    return competition


@access_token_required
def update_competiton(
    request: Request, db: Session, competition: CompetitionUpdateSchema, id: int
):
    comp = get_competition_by_id(request, db, id)
    if comp:
        comp.id = comp.id
        comp.name = competition.name
        db.add(comp)
        db.commit()
        db.refresh(comp)
        return {"updated_competition": comp, "message": "Competition is updated"}
    else:
        raise HTTPException(status_code=404, detail="competition not found")


def delete_competition(request: Request, db: Session, competition_id: int):
    com = get_competition_by_id(request, db, competition_id)
    if com:
        db.delete(com)
        db.commit()
        return "competition deleted"
    else:
        raise HTTPException(status_code=404, detail="competition not found")


@access_token_required
def delete_all_competition(request: Request, db: Session):
    db.query(Competition).delete()
    db.commit()


@access_token_required
def get_competiton_with_entry(request: Request, id: int, db: Session):
    competition = db.query(Competition).filter_by(id=id).first()
    if not competition:
        raise HTTPException(status_code=404, detail="competition not found")

    print(type(competition.entries))

    # check if user_id is null or not in entries tale
    entries = [
        i
        for i in competition.entries
        if i.user_id is not None and i.competition_id is not None
    ]

    competition_response = CompetitionResponse(
        name=competition.name, id=competition.id, entries=entries
    )
    return competition_response
