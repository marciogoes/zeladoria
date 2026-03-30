from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token, UsuarioUpdate
from app.utils.auth import create_access_token, get_current_user
from app.utils.rate_limit import check_rate_limit, get_client_ip, reset_attempts

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(
    request: Request,
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    # Rate limit: 5 registros por IP em 15 min (anti-spam)
    ip = get_client_ip(request)
    check_rate_limit(f"register:{ip}", max_attempts=5, window_seconds=900)

    if db.query(Usuario).filter(Usuario.email == usuario_data.email).first():
        raise HTTPException(400, "Email já cadastrado")

    usuario = Usuario(
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha=Usuario.hash_senha(usuario_data.senha),
        telefone=usuario_data.telefone,
        cpf=getattr(usuario_data, "cpf", None),
        tipo=usuario_data.tipo,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    access_token = create_access_token(data={"sub": str(usuario.id)})
    return {"access_token": access_token, "token_type": "bearer", "usuario": usuario}


@router.post("/login", response_model=Token)
def login(
    request: Request,
    login_data: UsuarioLogin,
    db: Session = Depends(get_db),
):
    # Rate limit: 10 tentativas por IP em 15 min (anti-brute-force)
    ip = get_client_ip(request)
    check_rate_limit(f"login:{ip}", max_attempts=10, window_seconds=900)

    # Rate limit adicional por email (5 tentativas em 15 min)
    check_rate_limit(f"login_email:{login_data.email}", max_attempts=5, window_seconds=900)

    usuario = db.query(Usuario).filter(Usuario.email == login_data.email).first()

    if not usuario or not usuario.verificar_senha(login_data.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )

    if not usuario.ativo:
        raise HTTPException(400, "Usuário inativo")

    # Login bem-sucedido — limpa contador por email
    reset_attempts(f"login_email:{login_data.email}")

    access_token = create_access_token(data={"sub": str(usuario.id)})
    return {"access_token": access_token, "token_type": "bearer", "usuario": usuario}


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UsuarioResponse)
def update_me(
    usuario_data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if usuario_data.nome:
        current_user.nome = usuario_data.nome
    if usuario_data.telefone:
        current_user.telefone = usuario_data.telefone
    db.commit()
    db.refresh(current_user)
    return current_user
