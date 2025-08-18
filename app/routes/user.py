from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import hash_password
from app.core.logging import log_audit, logger

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            logger.warning(f"Tentativa de criar usuário com email já existente: {user.email}")
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        db_user = User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Log de auditoria
        log_audit(
            user_id=current_user.id,
            action="CREATE",
            resource="USER",
            message=f"Usuário criado: {db_user.name} ({db_user.email})"
        )
        
        logger.info(f"Usuário criado com sucesso: {db_user.name}")
        return db_user
        
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(User).all()

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserCreate,  #TODO: Trocar por UserUpdate
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user_data = user.dict(exclude_unset=True)  # só pega os campos enviados

    # Se a senha for enviada, aplica o hash
    if "password" in user_data and user_data["password"]:
        user_data["password"] = hash_password(user_data["password"])

    for field, value in user_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    # Log de auditoria
    log_audit(
        user_id=current_user.id,
        action="UPDATE",
        resource="USER",
        message=f"Usuário atualizado: {db_user.name} ({db_user.email})"
    )

    logger.info(f"Usuário atualizado com sucesso: {db_user.name}")
    return db_user

@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return user

