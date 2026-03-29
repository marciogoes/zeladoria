from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse
from app.utils.auth import get_current_user, require_role

router = APIRouter()

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    tipo: Optional[str] = None,
    current_user: Usuario = Depends(require_role("gestor", "admin")),
    db: Session = Depends(get_db)
):
    query = db.query(Usuario)
    
    if tipo:
        query = query.filter(Usuario.tipo == tipo)
    
    usuarios = query.order_by(Usuario.nome).all()
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")
    
    return usuario
