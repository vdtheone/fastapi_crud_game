
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AuthSchema(BaseModel):
    id : int
    username : str
    email : str
    hashed_password :str
    is_active : bool
    created_at : datetime
    updated_at : datetime
 
    class Config:
        from_attributes = True


class AuthTotalCountSchema(BaseModel):
    total_user : Optional[int] = None



class AuthCreateSchema(BaseModel):
    username: str
    email : str
    hashed_password : str
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True


class AuthUpdateSchema(BaseModel):
    username: str
    email : str
    hashed_password : str
    updated_at : datetime
    class Config:
        form_attributes = True


class AuthLoginSchema(BaseModel):
    username:str
    password:str

    class Config:
        form_attributes = True
