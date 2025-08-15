from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleOut
from app.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.post("/", response_model=ScheduleOut)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_schedule = Schedule(**schedule.dict(), gestor_id=current_user.id)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.get("/", response_model=list[ScheduleOut])
def list_schedules(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Schedule).all()

#TODO: Implementar endpoints para atualizar e deletar agendamentos, além de filtrar por motorista ou veículo.