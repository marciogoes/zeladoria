"""
Sprint 6 — Transparência & Governo Aberto
API pública, orçamento participativo, auditoria
"""
from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.bairro import Bairro
from app.models.categoria import Categoria
from app.models.sprints_5_8 import (
    PropostaOrcamento, VotoProposta, RegistroAuditoria
)
from app.models.usuario import Usuario
from app.utils.auth import get_current_user, require_role
from app.utils.auditoria import registrar
from app.utils.rate_limit import check_rate_limit, get_client_ip

router = APIRouter(prefix="/api/transparencia", tags=["Transparência"])
router_publico = APIRouter(prefix="/api/publico", tags=["API Pública"])


# ─────────────────────────────────────────
# API PÚBLICA — sem autenticação, dados anonimizados
# ─────────────────────────────────────────
@router_publico.get("/chamados")
def chamados_publicos(
    request: Request,
    status: Optional[str] = None,
    bairro_id: Optional[int] = None,
    categoria_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Endpoint público — dados anonimizados para pesquisadores e jornalistas.
    Rate limit: 30 requisições por minuto por IP.
    """
    # Rate limit: 30 req/min por IP para evitar scraping
    ip = get_client_ip(request)
    check_rate_limit(f"publico:{ip}", max_attempts=30, window_seconds=60)

    limit = min(limit, 100)  # máx 100 (era 500 — redução de exposição)
    query = db.query(Chamado)
    if status:
        query = query.filter(Chamado.status == status)
    if bairro_id:
        query = query.filter(Chamado.bairro_id == bairro_id)
    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)

    total = query.count()
    chamados = query.order_by(Chamado.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "dados": [
            {
                "protocolo":   c.protocolo,
                "titulo":      c.titulo,
                "status":      c.status,
                "prioridade":  c.prioridade,
                "bairro":      c.bairro.nome if c.bairro else None,
                "categoria":   c.categoria.nome if c.categoria else None,
                "latitude":    c.latitude,
                "longitude":   c.longitude,
                "votos":       c.total_votos,
                "criado_em":   c.created_at.isoformat() if c.created_at else None,
                "resolvido_em":c.data_resolucao.isoformat() if c.data_resolucao else None,
            }
            for c in chamados
        ],
    }


@router_publico.get("/estatisticas")
def estatisticas_publicas(db: Session = Depends(get_db)):
    """Resumo público de zeladoria para painel em telão ou imprensa."""
    total = db.query(func.count(Chamado.id)).scalar() or 0
    resolvidos = db.query(func.count(Chamado.id)).filter(Chamado.status == "resolvido").scalar() or 0
    abertos = db.query(func.count(Chamado.id)).filter(Chamado.status == "aberto").scalar() or 0

    por_bairro = (
        db.query(Bairro.nome, func.count(Chamado.id).label("total"))
        .join(Chamado, Chamado.bairro_id == Bairro.id, isouter=True)
        .group_by(Bairro.id)
        .order_by(func.count(Chamado.id).desc())
        .limit(5).all()
    )

    por_categoria = (
        db.query(Categoria.nome, func.count(Chamado.id).label("total"))
        .join(Chamado, Chamado.categoria_id == Categoria.id, isouter=True)
        .group_by(Categoria.id)
        .order_by(func.count(Chamado.id).desc())
        .limit(5).all()
    )

    return {
        "total_chamados": total,
        "resolvidos": resolvidos,
        "abertos": abertos,
        "taxa_resolucao": round(resolvidos / total * 100, 1) if total else 0,
        "top_bairros": [{"bairro": b, "total": t} for b, t in por_bairro],
        "top_categorias": [{"categoria": c, "total": t} for c, t in por_categoria],
        "gerado_em": datetime.now(timezone.utc).isoformat(),
    }


# ─────────────────────────────────────────
# ORÇAMENTO PARTICIPATIVO
# ─────────────────────────────────────────
class PropostaCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    bairro_id: Optional[int] = None
    custo_estimado: Optional[float] = None
    encerra_em: Optional[datetime] = None


@router.get("/propostas")
def listar_propostas(
    status: Optional[str] = "votacao",
    db: Session = Depends(get_db),
):
    query = db.query(PropostaOrcamento).filter(PropostaOrcamento.ativa == True)
    if status:
        query = query.filter(PropostaOrcamento.status == status)
    propostas = query.order_by(PropostaOrcamento.total_votos.desc()).all()

    return [
        {
            "id": p.id,
            "titulo": p.titulo,
            "descricao": p.descricao,
            "categoria": p.categoria,
            "bairro": p.bairro.nome if p.bairro else None,
            "custo_estimado": p.custo_estimado,
            "total_votos": p.total_votos,
            "status": p.status,
            "encerra_em": p.encerra_em.isoformat() if p.encerra_em else None,
        }
        for p in propostas
    ]


@router.post("/propostas")
def criar_proposta(
    dados: PropostaCreate,
    current_user: Usuario = Depends(require_role("admin", "gestor", "secretaria")),
    db: Session = Depends(get_db),
):
    proposta = PropostaOrcamento(**dados.model_dump(), autor_id=current_user.id)
    db.add(proposta)
    db.flush()
    registrar(db, "PropostaOrcamento", proposta.id, "criada",
              {"titulo": proposta.titulo}, current_user.id)
    db.commit()
    return {"id": proposta.id, "titulo": proposta.titulo}


@router.post("/propostas/{proposta_id}/votar")
def votar_proposta(
    proposta_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    proposta = db.query(PropostaOrcamento).filter_by(id=proposta_id, ativa=True).first()
    if not proposta:
        raise HTTPException(404, "Proposta não encontrada")
    if proposta.status != "votacao":
        raise HTTPException(400, "Proposta não está em fase de votação")

    existente = db.query(VotoProposta).filter_by(
        usuario_id=current_user.id, proposta_id=proposta_id
    ).first()

    if existente:
        db.delete(existente)
        proposta.total_votos = max(0, proposta.total_votos - 1)
        db.commit()
        return {"votou": False, "total_votos": proposta.total_votos}

    db.add(VotoProposta(usuario_id=current_user.id, proposta_id=proposta_id))
    proposta.total_votos += 1
    registrar(db, "PropostaOrcamento", proposta_id, "votada", {}, current_user.id)
    db.commit()
    return {"votou": True, "total_votos": proposta.total_votos}


# ─────────────────────────────────────────
# AUDITORIA
# ─────────────────────────────────────────
@router.get("/auditoria")
def trilha_auditoria(
    entidade: Optional[str] = None,
    entidade_id: Optional[int] = None,
    limit: int = 50,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    query = db.query(RegistroAuditoria)
    if entidade:
        query = query.filter(RegistroAuditoria.entidade == entidade)
    if entidade_id:
        query = query.filter(RegistroAuditoria.entidade_id == entidade_id)

    blocos = query.order_by(RegistroAuditoria.id.desc()).limit(limit).all()
    return [
        {
            "id": b.id,
            "entidade": b.entidade,
            "entidade_id": b.entidade_id,
            "acao": b.acao,
            "dados": b.dados,
            "hash": b.hash_bloco[:16] + "…",
            "hash_anterior": b.hash_anterior[:16] + "…" if b.hash_anterior else None,
            "criado_em": b.criado_em.isoformat(),
        }
        for b in blocos
    ]


@router.get("/auditoria/verificar")
def verificar_integridade(
    current_user: Usuario = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    """Verifica se a cadeia de blocos não foi adulterada."""
    blocos = db.query(RegistroAuditoria).order_by(RegistroAuditoria.id.asc()).all()
    erros = []
    for b in blocos:
        esperado = RegistroAuditoria.calcular_hash(
            b.entidade, b.entidade_id, b.acao, b.dados, b.hash_anterior, b.criado_em
        )
        if esperado != b.hash_bloco:
            erros.append({"id": b.id, "entidade": b.entidade, "entidade_id": b.entidade_id})

    return {
        "total_blocos": len(blocos),
        "integro": len(erros) == 0,
        "blocos_comprometidos": erros,
    }
