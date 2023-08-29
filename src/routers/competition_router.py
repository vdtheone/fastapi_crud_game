from fastapi import APIRouter, Depends, Request
from src.models.competition import Competition
from src.config import SessionLocal
from sqlalchemy.orm import Session
from src.services.competition_crud import (
    create_competition,
    delete_all_competition,
    delete_competition,
    get_all_competition,
    get_competition_by_id,
    get_competiton_with_entry,
    update_competiton,
)
from src.schemas.competition import (
    CompetitionCreateSchema,
    CompetitionResponse,
    CompetitionSchema,
    CompetitionUpdateSchema,
)


competition_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@competition_router.get("/")
async def all_competition(request:Request, db: Session = Depends(get_db)):
    all_comp = get_all_competition(request, db, 0, 100)
    return all_comp


@competition_router.post("/create/")
async def create(request:Request, competition: CompetitionCreateSchema, db: Session = Depends(get_db)):
    new_competition = create_competition(request, db, competition)
    return {"competition": new_competition, "message": "competition created"}


@competition_router.get("/get/{id}", response_model=CompetitionSchema)
async def competition_by_id(request:Request, id: int, db: Session = Depends(get_db)):
    competition = get_competition_by_id(request, db, id)
    if competition is None:
        return {"message": "Not found"}
    else:
        return competition


@competition_router.put("/competition/{id}")
async def update(request:Request, id: int, competition: CompetitionUpdateSchema, db: Session = Depends(get_db)):
    updated_competition = update_competiton(request, db, competition, id)
    return updated_competition


@competition_router.delete("/delete/{id}")
async def delete(request:Request, id: int, db: Session = Depends(get_db)):
    deleted_competition = delete_competition(request, db, id)
    return {"message": deleted_competition}


@competition_router.delete("/delete_all/")
async def delete_all(request:Request, db: Session = Depends(get_db)):
    delete_all_competition(request, db)
    return {"message": "all competitions deleted"}


@competition_router.get("/competition/{id}", response_model=CompetitionResponse)
async def competition_by_id_with_entry(request:Request, id: int, db: Session = Depends(get_db)):
    competition_response = get_competiton_with_entry(request, id, db)
    return competition_response
