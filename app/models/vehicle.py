from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, unique=True, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer)
    current_mileage = Column(Integer, default=0)
    active = Column(Boolean, default=True)