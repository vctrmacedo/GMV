from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate
from app.models.user import User
from app.core.security import verify_password, create_access_token, hash_password
from app.database import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

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