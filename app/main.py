from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)