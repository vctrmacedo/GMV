from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    active: bool
    class Config:
        orm_mode = True