from pydantic import BaseModel


class EntrySchema(BaseModel):
    id: int
    user_id: int
    competition_id: int

    class Config:
        from_attributes = True


class EntryCreateSchema(BaseModel):
    user_id: int
    competition_id: int

    class Config:
        from_attributes = True


class EntryUpdateSchema(EntryCreateSchema):
    class Config:
        from_attributes = True
