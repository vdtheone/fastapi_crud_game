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

