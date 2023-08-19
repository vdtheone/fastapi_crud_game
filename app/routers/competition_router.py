
from fastapi import APIRouter, Depends
from app.config.config import SessionLocal
from sqlalchemy.orm import Session
from app.services.competition_crud import create_competition, delete_competition, get_all_competition, get_competition_by_id, update_competiton
from app.schemas.schema import CompetitionSchema, UserSchema
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


@competition_router.post('/create')
async def create(competition:CompetitionSchema, user_id: int, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        data = create_competition(db, db_user.id, competition)
        return data
    else:
        return {"message":"User not found for this id"}


@competition_router.get("/competition/{id}")
async def competition_by_id(id:int, db:Session = Depends(get_db)):
    competition = get_competition_by_id(db,id)
    return competition


@competition_router.put("/update/{id}")
async def update(id:int, competition:CompetitionSchema, user_id:int, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        data = update_competiton(db, competition, db_user.id, competition.name)
        return data
    else:
        return {"message":"Competition is not updated"}


@competition_router.delete("/delete/{id}")
async def delete(id:int, db:Session = Depends(get_db)):
    data = delete_competition(db,id)
    return {"message":"competition deleted"}
