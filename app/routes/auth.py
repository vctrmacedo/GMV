from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate
from app.models.user import User
from app.core.security import verify_password, create_access_token, hash_password
from app.database import get_db
from app.core.logging import log_security, log_audit, logger
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username_or_email: str  # Aceita tanto email quanto nome de usuário
    password: str

@router.post("/login")
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    try:
        # Buscar usuário por email OU por nome
        user = db.query(User).filter(
            (User.email == payload.username_or_email) | 
            (User.name == payload.username_or_email)
        ).first()
        
        if not user or not verify_password(payload.password, user.password):
            # Log de tentativa de login falhada
            log_security(
                event="LOGIN_FAILED",
                user_id=user.id if user else None,
                ip=request.client.host,
                details=f"Tentativa de login com credenciais inválidas: {payload.username_or_email}"
            )
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        
        # Log de login bem-sucedido
        log_security(
            event="LOGIN_SUCCESS",
            user_id=user.id,
            ip=request.client.host,
            details=f"Login bem-sucedido para usuário: {user.name}"
        )
        
        # Log de auditoria
        log_audit(
            user_id=user.id,
            action="LOGIN",
            resource="AUTH",
            message=f"Usuário fez login: {user.name}"
        )
        
        token = create_access_token({"sub": str(user.id)})
        logger.info(f"Token gerado para usuário: {user.name}")
        return {"access_token": token, "token_type": "bearer"}
        
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        raise

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se já existe algum usuário no sistema
    existing_user = db.query(User).first()
    if existing_user:
        raise HTTPException(status_code=403, detail="Registro inicial já foi realizado")
    
    # Verificar se o email já existe
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar o primeiro usuário (sem verificação de token)
    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#TODO implementar o logout e a verificação do token de autenticação.