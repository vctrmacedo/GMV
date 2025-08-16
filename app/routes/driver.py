from re import U
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

@router.delete("/{driver_id}", response_model=DriverOut)
def delete_driver(driver_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    db.delete(driver)
    db.commit()
    return driver

@router.put("/{driver_id}", response_model=DriverOut)
def update_driver(driver_id: int, driver: DriverCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    for field, value in driver.dict().items():
        setattr(db_driver, field, value)
    db.commit()
    db.refresh(db_driver)
    return db_driver


#TODO implementar a atualização e exclusão de motoristas, além de outras funcionalidades necessárias.