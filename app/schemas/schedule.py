from pydantic import BaseModel
from datetime import date
from typing import Optional

class ScheduleBase(BaseModel):
    driver_id: int
    vehicle_id: int
    departure_date: date
    return_date: date
    origin: str
    destination: str
    km_initial: Optional[int] = 0
    km_final: Optional[int] = 0
    liters_fuel: Optional[float] = 0
    fuel_cost: Optional[float] = 0
    observations: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleOut(ScheduleBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True