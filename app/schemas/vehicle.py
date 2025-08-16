from pydantic import BaseModel

class VehicleBase(BaseModel):
    license_plate: str
    modelo: str
    year: int
    current_mileage: int = 0

class VehicleCreate(VehicleBase):
    pass

class VehicleOut(VehicleBase):
    id: int
    active: bool
    class Config:
        from_attributes = True