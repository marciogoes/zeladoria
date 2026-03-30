"""
Sprint 18 — Gestão de Usuários (Admin)
CRUD completo: listar, detalhar, ativar/desativar, alterar tipo, resetar senha.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse
from app.utils.auth import get_current_user, require_role

router = APIRouter()


# ── Schemas de gestão ─────────────────────────────────────────────────────────

class UsuarioAdminUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    ativo: Optional[bool] = None
    secretaria_id: Optional[int] = None


class ResetSenhaAdmin(BaseModel):
    nova_senha: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    tipo: Optional[str] = None,
    ativo: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: Usuario = Depends(require_role("gestor", "admin")),
    db: Session = Depends(get_db),
):
    query = db.query(Usuario)

    if tipo:
        query = query.filter(Usuario.tipo == tipo)
    if ativo is not None:
        query = query.filter(Usuario.ativo == ativo)
    if search:
        query = query.filter(
            (Usuario.nome.ilike(f"%{search}%")) |
            (Usuario.email.ilike(f"%{search}%"))
        )

    return query.order_by(Usuario.nome).all()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioAdminUpdate,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """Atualiza nome, tipo, status ou secretaria de um usuário."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    # Gestor só pode gerenciar cidadãos e equipes
    if current_user.tipo == "gestor" and usuario.tipo in ("admin", "gestor"):
        raise HTTPException(403, "Gestores não podem alterar outros gestores ou admins")

    if dados.nome is not None:
        usuario.nome = dados.nome
    if dados.tipo is not None:
        _TIPOS_VALIDOS = ("cidadao", "equipe", "secretaria", "gestor", "admin")
        if dados.tipo not in _TIPOS_VALIDOS:
            raise HTTPException(400, f"Tipo inválido. Use: {', '.join(_TIPOS_VALIDOS)}")
        # Apenas admin pode promover para admin
        if dados.tipo == "admin" and current_user.tipo != "admin":
            raise HTTPException(403, "Apenas admin pode promover para admin")
        usuario.tipo = dados.tipo
    if dados.ativo is not None:
        usuario.ativo = dados.ativo
    if dados.secretaria_id is not None:
        usuario.secretaria_id = dados.secretaria_id

    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/{usuario_id}/ativar", response_model=UsuarioResponse)
def ativar_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")
    usuario.ativo = True
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/{usuario_id}/desativar", response_model=UsuarioResponse)
def desativar_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")
    if usuario.id == current_user.id:
        raise HTTPException(400, "Você não pode desativar sua própria conta")
    usuario.ativo = False
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/{usuario_id}/reset-senha")
def resetar_senha(
    usuario_id: int,
    dados: ResetSenhaAdmin,
    current_user: Usuario = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """Apenas admin pode resetar senha de qualquer usuário."""
    if len(dados.nova_senha) < 6:
        raise HTTPException(400, "Senha deve ter pelo menos 6 caracteres")

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")

    usuario.senha = Usuario.hash_senha(dados.nova_senha)
    db.commit()
    return {"mensagem": f"Senha de {usuario.nome} redefinida com sucesso"}


@router.get("/stats/resumo")
def resumo_usuarios(
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """Resumo de usuários por tipo e status para o painel admin."""
    from sqlalchemy import func
    por_tipo = db.query(
        Usuario.tipo,
        func.count(Usuario.id).label("total"),
        func.sum(Usuario.ativo.cast(db.bind.dialect.name == "sqlite" and "INTEGER" or "INTEGER")).label("ativos"),
    ).group_by(Usuario.tipo).all()

    total_geral = db.query(func.count(Usuario.id)).scalar() or 0
    total_ativos = db.query(func.count(Usuario.id)).filter(Usuario.ativo == True).scalar() or 0

    return {
        "total": total_geral,
        "ativos": total_ativos,
        "inativos": total_geral - total_ativos,
        "por_tipo": [
            {"tipo": t, "total": total}
            for t, total, _ in por_tipo
        ],
    }
