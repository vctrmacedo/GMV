from pydantic import BaseModel
from datetime import date

class DriverBase(BaseModel):
    name: str
    cpf: str
    phone: str = None
    cnh_category: str
    cnh_validity: date

class DriverCreate(DriverBase):
    pass

class DriverOut(DriverBase):
    id: int
    active: bool
    class Config:
        from_attributes = True
