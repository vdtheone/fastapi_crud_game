from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config import SessionLocal
from src.services.entry_crud import create_entry, delete_all_entry, delete_entry, get_all_entries, get_entry_by_id, update_entry
from src.models.user import User
from src.models.competition import Competition
from src.schemas.entry import EntryCreateSchema, EntryUpdateSchema

entry_router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


@entry_router.get("/")
async def get(db:Session = Depends(get_db)):
    all_entries = get_all_entries(db,0,100)
    return all_entries


@entry_router.post("/create/")
async def create(entry:EntryCreateSchema, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==entry.user_id).first()
    competition = db.query(Competition).filter(Competition.id == entry.competition_id).first()
    
    if user and competition:
        new_entry = create_entry(user.id,competition.id,db)
        return {"entry":new_entry, "message":"new entry created"}
    else:
        return {"message":"Error"}


@entry_router.get("/entry/{entry_id}")
async def get_entry(entry_id:int, db:Session = Depends(get_db)):
    one_entry = get_entry_by_id(db,entry_id)
    return one_entry


@entry_router.put("/update/{id}")
async def update(id:int ,entry:EntryUpdateSchema , db:Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id==entry.user_id).first()
    competition = db.query(Competition).filter(Competition.id == entry.competition_id).first()
    
    if user and competition:
        new_entry = update_entry(id,user.id,competition.id,db)
        return new_entry
    else:
        return {"message":"Error"}


@entry_router.delete("/delete/{id}")
async def delete(id:int, db:Session = Depends(get_db)):
    message = delete_entry(id,db)
    return {"message":message}



@entry_router.delete("/delete_all/")
async def delete_all(db:Session = Depends(get_db)):
    delete_all_entry(db)
    return {"message":"all entries deleted"}



