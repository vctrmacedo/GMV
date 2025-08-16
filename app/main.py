from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import auth, user, driver, vehicle, schedule
from app.core.logging import logger, log_request_middleware

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Configurar aplicação
app = FastAPI(
    title="Sistema de Gestão de Frota",
    description="API completa para gestão de frota empresarial",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de logging
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await log_request_middleware(request, call_next)

# Incluir rotas
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(driver.router)
app.include_router(vehicle.router)
app.include_router(schedule.router)

# Eventos de startup/shutdown
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Sistema de Gestão de Frota iniciado com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Sistema de Gestão de Frota finalizado.")