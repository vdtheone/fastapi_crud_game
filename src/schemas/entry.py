from pydantic import BaseModel


class EntrySchema(BaseModel):
    id: int
    user_id: int
    competition_id: int

    class Config:
        orm_mode = True


class EntryCreateSchema(BaseModel):
    user_id: int
    competition_id: int

    class Config:
        orm_mode = True


class EntryUpdateSchema(EntryCreateSchema):
    class Config:
        orm_mode = True



