from pydantic import BaseModel

# Modelo base comum
class VehicleBase(BaseModel):
    license_plate: str
    model: str
    year: int
    current_mileage: int = 0
    active: bool = True  # Define como booleano desde o início

# Para criação
class VehicleCreate(VehicleBase):
    pass

# Para saída (GET)
class VehicleOut(VehicleBase):
    id: int

    class Config:
        from_attributes = True
