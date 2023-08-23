
from datetime import datetime
from pydantic import BaseModel


class AuthSchema(BaseModel):
    
    username: str
    email : str
    hashed_password : str
    created_at : datetime
    updated_at : datetime
 

    class Config:
        from_attributes = True