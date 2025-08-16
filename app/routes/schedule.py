from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleOut
from app.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.post("/", response_model=ScheduleOut)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_schedule = Schedule(**schedule.dict(), user_id=current_user.id)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.get("/", response_model=list[ScheduleOut])
def list_schedules(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Schedule).all()

@router.put("/{schedule_id}", response_model=ScheduleOut)
def update_schedule(schedule_id: int, schedule: ScheduleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    for field, value in schedule.dict().items():
        setattr(db_schedule, field, value)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}", response_model=ScheduleOut)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    db.delete(schedule)
    db.commit()
    return schedule

#TODO: Implementar endpoints para atualizar e deletar agendamentos, além de filtrar por motorista ou veículo.