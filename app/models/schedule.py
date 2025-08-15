from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    departure_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    km_initial = Column(Integer)
    km_final = Column(Integer)
    liters_fuel = Column(Float)
    fuel_cost = Column(Float)
    observations = Column(Text, length=500)

    driver = relationship("Driver")
    vehicle = relationship("Vehicle")
    user = relationship("User")