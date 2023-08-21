from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True


class UserUpdateSchema(UserCreateSchema):
    class Config:
        orm_mode = True


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



