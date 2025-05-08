from pydantic import BaseModel, EmailStr
from typing import Literal

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role:str

class UserDB(UserLogin):
    role: Literal["admin", "user"]
