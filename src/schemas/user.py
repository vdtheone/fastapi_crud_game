from datetime import date

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    auth_id: int
    name: str
    age: int
    gender: str
    age: int
    date_of_birth: date

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    # auth_id : int
    name: str
    age: int
    gender: str
    date_of_birth: date

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: str
    age: int
    gender: str
    date_of_birth: date

    class Config:
        from_attributes = True


class UserWithEntry(BaseModel):
    id: int
    name: str
    # competition : List[EntrySchema]
    competition: list
    # competition : list
