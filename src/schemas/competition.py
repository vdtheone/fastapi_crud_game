from pydantic import BaseModel


class CompetitionSchema(BaseModel):
    id: int
    user_id: int
    name: str

    class Config:
        orm_mode = True


class CompetitionCreateSchema(BaseModel):
    user_id: int
    name: str

    class Config:
        orm_mode = True


class CompetitionUpdateSchema(CompetitionCreateSchema):
    class Config:
        orm_mode = True






