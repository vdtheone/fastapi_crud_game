from pydantic import BaseModel


class CompetitionSchema(BaseModel):
    id: int
    user_id: int
    name: str

    class Config:
        from_attributes = True


class CompetitionCreateSchema(BaseModel):
    user_id: int
    name: str

    class Config:
        from_attributes = True


class CompetitionUpdateSchema(CompetitionCreateSchema):
    class Config:
        from_attributes = True






