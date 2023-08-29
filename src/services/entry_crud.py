from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from src.models.competition import Competition
from src.models.user import User
from src.schemas.entry import EntryCreateSchema, EntryUpdateSchema
from src.models.entry import Entry
from src.utils.return_jwt_token import access_token_required
from jose import jwt
import os


SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


@access_token_required
def get_all_entries(request:Request, db: Session, skip: int = 0, limit: int = 100):
    return db.query(Entry).offset(skip).limit(limit).all()

@access_token_required
def create_entry(request:Request, entry:EntryCreateSchema, db: Session):
    user = db.query(User).filter(User.id == entry.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    competition = (
        db.query(Competition).filter(Competition.id == entry.competition_id).first()
    ) 
    if competition is None:
        raise HTTPException(status_code=404, detail="competition not found")
    
    new_entry = Entry(user_id=user.id, competition_id=competition.id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@access_token_required
def get_entry_by_id(request:Request, db: Session, entry_id: int):
    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="entry not found")
    return entry


def update_entry(request:Request, entry_id: int, entry: EntryUpdateSchema, db: Session):
    access_token = request.headers.get("Authorization")
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(User).filter(User.id == entry.user_id, User.auth_id == payload.get('id')).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    competition = (
        db.query(Competition).filter(Competition.id == entry.competition_id).first()
    )
    if competition is None:
        raise HTTPException(status_code=404, detail="competition not found")

    update_entry = get_entry_by_id(request, db, entry_id)
    update_entry.id = entry_id
    update_entry.competition_id = competition.id
    update_entry.user_id = user.id
    db.add(update_entry)
    db.commit()
    db.refresh(update_entry)
    return update_entry


def delete_entry(request:Request, entry_id: int, db: Session):
    entry = get_entry_by_id(request, db, entry_id)
    db.delete(entry)
    db.commit()
    return {"message": "entry deleted"}
    

@access_token_required
def delete_all_entry(request:Request, db: Session):
    db.query(Entry).delete()
    db.commit()
