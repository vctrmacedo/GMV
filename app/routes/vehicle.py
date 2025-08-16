from fastapi import APIRouter, Depends, HTTPException
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

@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(vehicle_id: int, vehicle: VehicleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    for field, value in vehicle.dict().items():
        setattr(db_vehicle, field, value)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.delete("/{vehicle_id}", response_model=VehicleOut)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    db.delete(vehicle)
    db.commit()
    return vehicle