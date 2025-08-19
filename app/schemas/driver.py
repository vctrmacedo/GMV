from pydantic import BaseModel
from datetime import date

class DriverBase(BaseModel):
    name: str
    cpf: str
    phone: str | None = None
    cnh_category: str
    cnh_validity: date
    active: bool | int = True  

class DriverCreate(DriverBase):
    pass

class DriverOut(DriverBase):
    id: int
    class Config:
        from_attributes = True