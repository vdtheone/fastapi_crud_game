
from datetime import datetime
from pydantic import BaseModel


class AuthSchema(BaseModel):
    name : str
    username: str
    email : str
    hashed_password : str
    gender : str
    date_of_birth : datetime
    age : int
    is_active : bool
    created_at : datetime
    updated_at : datetime
 

    class Config:
        orm_mode = True