from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True


class CompetitionSchema(BaseModel):
    id: int
    user_id: int
    name: str

    class Config:
        orm_mode = True


class EntrySchema(BaseModel):
    id: int
    user_id: int
    competition_id: int

    class Config:
        orm_mode = True



