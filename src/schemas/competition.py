from typing import List
from pydantic import BaseModel

from src.schemas.entry import EntrySchema

# from src.schemas.user import UserSchema


class CompetitionSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CompetitionCreateSchema(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CompetitionUpdateSchema(CompetitionCreateSchema):
    class Config:
        from_attributes = True


class CompetitionResponse(BaseModel):
    name: str
    id: int
    entries: List[EntrySchema]
    






