from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token, UsuarioUpdate
from app.utils.auth import create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar se email já existe
    if db.query(Usuario).filter(Usuario.email == usuario_data.email).first():
        raise HTTPException(400, "Email já cadastrado")
    
    # Criar usuário
    usuario = Usuario(
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha=Usuario.hash_senha(usuario_data.senha),
        telefone=usuario_data.telefone,
        cpf=usuario_data.cpf,
        tipo=usuario_data.tipo
    )
    
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    # Gerar token
    access_token = create_access_token(data={"sub": str(usuario.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }

@router.post("/login", response_model=Token)
def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    # Buscar usuário
    usuario = db.query(Usuario).filter(Usuario.email == login_data.email).first()
    
    if not usuario or not usuario.verificar_senha(login_data.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not usuario.ativo:
        raise HTTPException(400, "Usuário inativo")
    
    # Gerar token
    access_token = create_access_token(data={"sub": str(usuario.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }

@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UsuarioResponse)
def update_me(
    usuario_data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if usuario_data.nome:
        current_user.nome = usuario_data.nome
    if usuario_data.telefone:
        current_user.telefone = usuario_data.telefone
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
