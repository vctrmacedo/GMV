from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverOut
from app.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=DriverOut)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_driver = Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

@router.get("/", response_model=list[DriverOut])
def list_drivers(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Driver).all()

#TODO implementar a atualização e exclusão de motoristas, além de outras funcionalidades necessárias.