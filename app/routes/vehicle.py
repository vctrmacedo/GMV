from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleOut
from app.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleOut)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.get("/", response_model=list[VehicleOut])
def list_vehicles(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Vehicle).all()

#TODO implementar a atualização e exclusão de veículos, além de outras funcionalidades necessárias.