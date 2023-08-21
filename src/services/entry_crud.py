from src.schemas.entry import EntrySchema
from sqlalchemy.orm import Session
from src.models.entry import Entry


def get_all_entries(db:Session, skip:int = 0, limit:int = 100):
    return db.query(Entry).offset(skip).limit(limit).all()


def create_entry(user_id:int, competition_id:int, db:Session):
    new_entry = Entry(user_id = user_id, competition_id = competition_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


def get_entry_by_id(db:Session, entry_id:int):
    return db.query(Entry).filter(Entry.id==entry_id).first()


def update_entry(entry_id:int, user_id:int, competition_id:int, db:Session):
    update_entry = get_entry_by_id(db,entry_id)
    update_entry.id = entry_id
    update_entry.competition_id = competition_id
    update_entry.user_id = user_id
    db.add(update_entry)
    db.commit()
    db.refresh(update_entry)
    return update_entry


def delete_entry(entry_id:int, db:Session):
    entry = get_entry_by_id(db,entry_id)
    if entry:
        db.delete(entry)
        db.commit()
        return "entry deleted"
    else:
        return "Entry not found"


def delete_all_entry(db:Session):
    all = db.query(Entry).delete()
    db.commit()
