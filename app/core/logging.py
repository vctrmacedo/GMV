import sys
from pathlib import Path
from loguru import logger
from datetime import datetime
from fastapi import Request
from starlette.responses import Response

# Criar diretório de logs se não existir
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configurar o logger principal
logger.remove()  # Remove configuração padrão

# Log para console (desenvolvimento)
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Log para arquivo (produção)
logger.add(
    log_dir / "app_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="1 day",        # Novo arquivo por dia
    retention="30 days",     # Manter por 30 dias
    compression="zip",       # Comprimir arquivos antigos
    enqueue=True             # Thread-safe
)

# Log de erros separado
logger.add(
    log_dir / "errors_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="1 day",
    retention="90 days",     # Erros ficam mais tempo
    compression="zip",
    enqueue=True
)

# Log de auditoria
logger.add(
    log_dir / "audit_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | AUDIT | {extra[user_id]} | {extra[action]} | "
           "{extra[resource]} | {message}",
    level="INFO",
    rotation="1 day",
    retention="365 days",    # Auditoria fica 1 ano
    compression="zip",
    enqueue=True,
    filter=lambda record: "audit" in record["extra"]
)

# Log de performance
logger.add(
    log_dir / "performance_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | PERF | {extra[endpoint]} | {extra[duration]}ms | {message}",
    level="INFO",
    rotation="1 day",
    retention="30 days",
    compression="zip",
    enqueue=True,
    filter=lambda record: "performance" in record["extra"]
)

# ============================
# Funções auxiliares de log
# ============================

def log_audit(user_id: int, action: str, resource: str, message: str, **kwargs):
    """Log de auditoria para operações CRUD"""
    logger.bind(audit=True, user_id=user_id, action=action, resource=resource).info(message, **kwargs)

def log_performance(endpoint: str, duration: float, message: str, **kwargs):
    """Log de performance para endpoints"""
    logger.bind(performance=True, endpoint=endpoint, duration=int(duration * 1000)).info(message, **kwargs)

def log_security(event: str, user_id: int = None, ip: str = None, **kwargs):
    """Log de eventos de segurança"""
    extra = {"security": True, "user_id": user_id, "ip": ip}
    logger.bind(**extra).warning(f"SECURITY: {event}", **kwargs)

def log_business(operation: str, details: dict, **kwargs):
    """Log de operações de negócio"""
    logger.info(f"BUSINESS: {operation} - {details}", **kwargs)

# ============================
# Middleware de logging
# ============================

async def log_request_middleware(request: Request, call_next):
    """Middleware para log automático de requests"""
    start_time = datetime.now()

    # Log do request
    logger.info(f"Request: {request.method} {request.url.path} - Client: {request.client.host}")

    # Processar request (precisa de await!)
    response: Response = await call_next(request)

    # Calcular duração
    duration = (datetime.now() - start_time).total_seconds()

    # Log da resposta
    logger.info(f"Response: {response.status_code} - Duration: {duration:.3f}s")

    # Log de performance se demorou muito
    if duration > 1.0:  # Mais de 1 segundo
        log_performance(
            endpoint=request.url.path,
            duration=duration,
            message=f"Slow request: {request.method} {request.url.path}"
        )

    return response

