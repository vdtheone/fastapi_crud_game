
from fastapi import APIRouter, Depends
from app.config.config import SessionLocal
from sqlalchemy.orm import Session
from app.services.competition_crud import create_competition, delete_all_competition, delete_competition, get_all_competition, get_competition_by_id, update_competiton
from app.schemas.schema import CompetitionCreateSchema, CompetitionSchema, CompetitionUpdateSchema
from app.models.models import User


competition_router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


@competition_router.get("/")
async def all_competition(db:Session = Depends(get_db)):
    all_comp = get_all_competition(db,0,100)
    return all_comp


@competition_router.post('/create/')
async def create(competition:CompetitionCreateSchema, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == competition.user_id).first()
    if db_user:
        new_competition = create_competition(db, competition)
        return {"competition":new_competition, "message":"competition created"}
    else:
        return {"message":"User not found for this id"}


@competition_router.get("/competition/{id}", response_model=CompetitionSchema)
async def competition_by_id(id:int, db:Session = Depends(get_db)):
    competition = get_competition_by_id(db,id)
    return competition


@competition_router.put("/update/{id}")
async def update(id:int, competition:CompetitionUpdateSchema, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == competition.user_id).first()
    if db_user:
        updated_competition = update_competiton(db, competition, id)
        return {"updated_competition":updated_competition, "message":"Competition is updated"}
    else:
        return {"message":"Competition is not updated"}


@competition_router.delete("/delete/{id}")
async def delete(id:int, db:Session = Depends(get_db)):
    deleted_competition = delete_competition(db,id)
    return {"message":"competition deleted"}


@competition_router.delete("/delete_all/")
async def delete_all(db:Session = Depends(get_db)):
    delete_all_competition(db)
    return {"message":"all competitions deleted"}
