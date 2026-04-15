from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.usuario import Usuario
from threading import Lock
import os

# Configurações JWT — SECRET_KEY vem do ambiente em produção
SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY or SECRET_KEY.startswith("sua-chave"):
    import secrets
    _generated = secrets.token_urlsafe(32)
    import logging
    logging.getLogger("zelo").warning(
        "SECRET_KEY não configurada ou usa valor placeholder! "
        "Defina SECRET_KEY no ambiente. Usando chave aleatória temporária (tokens inválidos após restart)."
    )
    SECRET_KEY = _generated

ALGORITHM = "HS256"
# 8 horas para usuários comuns — muito mais seguro que 30 dias
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRATION", str(8 * 60)))

# Blacklist de tokens revogados (logout) — em memória
# Para multi-worker: migre para Redis SET com TTL igual ao ACCESS_TOKEN_EXPIRE_MINUTES
_blacklist: set[str] = set()
_blacklist_lock = Lock()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    # Verifica blacklist antes de decodificar
    with _blacklist_lock:
        if token in _blacklist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revogado (logout realizado)"
            )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


def revoke_token(token: str) -> None:
    """Adiciona o token à blacklist (logout). Expira naturalmente com o token."""
    with _blacklist_lock:
        _blacklist.add(token)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo"
        )
    return usuario

def require_role(*roles):
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.tipo not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Sem permissão. Requer um dos perfis: {', '.join(roles)}"
            )
        return current_user
    return role_checker
