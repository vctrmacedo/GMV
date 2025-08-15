from sqlalchemy import Column, Integer, String, Boolean, Date
from app.database import Base

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf = Column(String, unique=True)
    phone = Column(String)
    cnh_category = Column(String)
    cnh_validity = Column(Date)
    active = Column(Boolean, default=True)