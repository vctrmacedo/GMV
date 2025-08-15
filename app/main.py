from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, user, driver, vehicle, schedule

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestão de Frota")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(driver.router)
app.include_router(vehicle.router)
app.include_router(schedule.router)