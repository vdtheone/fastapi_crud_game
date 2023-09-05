from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.config import SessionLocal
from src.schemas.entry import EntryCreateSchema, EntryUpdateSchema
from src.services.entry_crud import (
    create_entry,
    delete_all_entry,
    delete_entry,
    get_all_entries,
    get_entry_by_id,
    update_entry,
)

entry_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@entry_router.get("/")
async def get(request: Request, db: Session = Depends(get_db)):
    all_entries = get_all_entries(request, db, 0, 100)
    return all_entries


@entry_router.post("/create/")
async def create(
    request: Request, entry: EntryCreateSchema, db: Session = Depends(get_db)
):
    new_entry = create_entry(request, entry, db)
    return new_entry


@entry_router.get("/entry/{entry_id}")
async def get_entry(request: Request, entry_id: int, db: Session = Depends(get_db)):
    one_entry = get_entry_by_id(request, db, entry_id)
    return one_entry


@entry_router.put("/update/{id}")
async def update(
    request: Request, id: int, entry: EntryUpdateSchema, db: Session = Depends(get_db)
):
    new_entry = update_entry(request, id, entry, db)
    return new_entry


@entry_router.delete("/delete/{id}")
async def delete(request: Request, id: int, db: Session = Depends(get_db)):
    message = delete_entry(request, id, db)
    return message


@entry_router.delete("/delete_all/")
async def delete_all(request: Request, db: Session = Depends(get_db)):
    delete_all_entry(request, db)
    return {"message": "all entries deleted"}
