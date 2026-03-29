"""
Router para o Catálogo Completo de Serviços
Usa a tabela servicos_secretaria (ServicoSecretaria model)
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List
from pydantic import BaseModel

from app.database.database import get_db
from app.models_servicos import ServicoSecretaria, PrioridadeServico, StatusServico

router = APIRouter(prefix="/api/catalogo", tags=["Catálogo Completo"])


# ── Schemas ──────────────────────────────────────────────────────────────────

class ServicoResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    secretaria_id: Optional[int] = None
    sla_horas: int
    prioridade: str
    status: str

    class Config:
        from_attributes = True


class EstatisticasResponse(BaseModel):
    total_servicos: int
    total_categorias: int
    servicos_emergenciais: int
    sla_medio: float
    por_prioridade: dict
    por_categoria: List[dict]


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ServicoResponse])
def listar_todos_servicos(
    busca: Optional[str] = None,
    secretaria_id: Optional[int] = None,
    prioridade: Optional[str] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ServicoSecretaria).filter(ServicoSecretaria.ativo == True)

    if busca:
        f = f"%{busca}%"
        query = query.filter(
            or_(
                ServicoSecretaria.nome.ilike(f),
                ServicoSecretaria.descricao.ilike(f),
                ServicoSecretaria.codigo.ilike(f),
                ServicoSecretaria.categoria.ilike(f),
            )
        )
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    if prioridade:
        query = query.filter(ServicoSecretaria.prioridade == prioridade)
    if categoria:
        query = query.filter(ServicoSecretaria.categoria.ilike(f"%{categoria}%"))

    return query.order_by(ServicoSecretaria.codigo).all()


@router.get("/servico/{codigo}", response_model=ServicoResponse)
def obter_servico_por_codigo(codigo: str, db: Session = Depends(get_db)):
    servico = db.query(ServicoSecretaria).filter_by(codigo=codigo.upper(), ativo=True).first()
    if not servico:
        raise HTTPException(404, f"Serviço '{codigo}' não encontrado")
    return servico


@router.get("/estatisticas", response_model=EstatisticasResponse)
def obter_estatisticas(db: Session = Depends(get_db)):
    base = db.query(ServicoSecretaria).filter(ServicoSecretaria.ativo == True)

    total = base.count()
    emergenciais = base.filter(ServicoSecretaria.prioridade == "emergencial").count()
    sla_medio = db.query(func.avg(ServicoSecretaria.sla_horas)).filter(
        ServicoSecretaria.ativo == True
    ).scalar() or 0

    por_prioridade = {}
    for p in PrioridadeServico:
        por_prioridade[p.value] = base.filter(ServicoSecretaria.prioridade == p).count()

    categorias_raw = (
        db.query(ServicoSecretaria.categoria, func.count(ServicoSecretaria.id).label("total"))
        .filter(ServicoSecretaria.ativo == True)
        .group_by(ServicoSecretaria.categoria)
        .order_by(func.count(ServicoSecretaria.id).desc())
        .all()
    )

    total_cats = db.query(func.count(func.distinct(ServicoSecretaria.categoria))).scalar() or 0

    return {
        "total_servicos": total,
        "total_categorias": total_cats,
        "servicos_emergenciais": emergenciais,
        "sla_medio": round(float(sla_medio), 2),
        "por_prioridade": por_prioridade,
        "por_categoria": [{"categoria": c, "total": t} for c, t in categorias_raw],
    }


@router.get("/categorias")
def listar_categorias(
    secretaria_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(
        ServicoSecretaria.categoria,
        func.count(ServicoSecretaria.id).label("total"),
    ).filter(ServicoSecretaria.ativo == True)

    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)

    return [
        {"categoria": cat, "total": total}
        for cat, total in query.group_by(ServicoSecretaria.categoria).all()
    ]


@router.get("/prioridades")
def listar_prioridades(db: Session = Depends(get_db)):
    resultado = (
        db.query(
            ServicoSecretaria.prioridade,
            func.count(ServicoSecretaria.id).label("total"),
            func.avg(ServicoSecretaria.sla_horas).label("sla_medio"),
        )
        .filter(ServicoSecretaria.ativo == True)
        .group_by(ServicoSecretaria.prioridade)
        .all()
    )
    ORDEM = {"emergencial": 1, "alta": 2, "media": 3, "baixa": 4, "agendavel": 5}
    return sorted(
        [{"prioridade": p, "total": t, "sla_medio_horas": round(float(s or 0), 1)} for p, t, s in resultado],
        key=lambda x: ORDEM.get(x["prioridade"], 99),
    )


@router.get("/buscar")
def buscar_servicos(
    q: str = Query(..., min_length=2),
    limite: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    f = f"%{q}%"
    servicos = (
        db.query(ServicoSecretaria)
        .filter(
            ServicoSecretaria.ativo == True,
            or_(
                ServicoSecretaria.nome.ilike(f),
                ServicoSecretaria.descricao.ilike(f),
                ServicoSecretaria.codigo.ilike(f),
                ServicoSecretaria.categoria.ilike(f),
            ),
        )
        .limit(limite)
        .all()
    )

    return [
        {
            "id": s.id,
            "codigo": s.codigo,
            "nome": s.nome,
            # descricao pode ser None — guarda com fallback antes de fatiar
            "descricao": ((s.descricao or "")[:100] + "…") if s.descricao and len(s.descricao) > 100 else (s.descricao or ""),
            "categoria": s.categoria,
            "sla_horas": s.sla_horas,
            "prioridade": s.prioridade.value if hasattr(s.prioridade, "value") else s.prioridade,
        }
        for s in servicos
    ]
