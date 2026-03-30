"""
Sprint 17 — Chamados com Paginação, Histórico e Export CSV
"""
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query, Response, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date
from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.usuario import Usuario
from app.models.historico import ChamadoHistorico, registrar_historico
from app.schemas.chamado import ChamadoCreate, ChamadoResponse, ChamadoUpdate, ChamadoAvaliar
from app.utils.auth import get_current_user
from app.utils.upload import save_upload_file
from app.utils.email_notif import notificar_criacao, notificar_mudanca_status
from pydantic import BaseModel

router = APIRouter()


# ─── Schemas locais ──────────────────────────────────────────────────────────

class ReclassificarChamado(BaseModel):
    servico_codigo: str
    servico_nome: str
    categoria: str
    sla_horas: int
    prioridade: str


class StatusUpdate(BaseModel):
    status: str


class PrioridadeUpdate(BaseModel):
    prioridade: str


class ChamadosPaginados(BaseModel):
    total: int
    pagina: int
    paginas: int
    limit: int
    items: List[ChamadoResponse]

    model_config = {"from_attributes": True}


# ─── Listagem com paginação ───────────────────────────────────────────────────

@router.get("/", response_model=ChamadosPaginados)
def listar_chamados(
    # Filtros
    status: Optional[str] = None,
    prioridade: Optional[str] = None,
    categoria_id: Optional[int] = None,
    bairro_id: Optional[int] = None,
    search: Optional[str] = None,
    # Sprint 18: Filtros de data
    data_inicio: Optional[date] = Query(default=None, description="Data inicial YYYY-MM-DD"),
    data_fim: Optional[date] = Query(default=None, description="Data final YYYY-MM-DD"),
    # Paginação
    pagina: int = Query(default=1, ge=1, description="Número da página (começa em 1)"),
    limit: int = Query(default=20, ge=1, le=200, description="Itens por página (máx. 200)"),
    # Ordenação
    ordem: str = Query(default="recente", regex="^(recente|antigo|prioridade|status)$"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Chamado)

    # Filtros
    if status:
        query = query.filter(Chamado.status == status)
    if prioridade:
        query = query.filter(Chamado.prioridade == prioridade)
    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)
    if bairro_id:
        query = query.filter(Chamado.bairro_id == bairro_id)
    if search:
        query = query.filter(
            (Chamado.protocolo.ilike(f"%{search}%")) |
            (Chamado.titulo.ilike(f"%{search}%"))
        )

    # Cidadão só vê seus chamados
    if current_user.tipo == "cidadao":
        query = query.filter(Chamado.usuario_id == current_user.id)

    # Sprint 18: Filtros de data
    if data_inicio:
        from datetime import datetime as dt
        query = query.filter(Chamado.created_at >= dt.combine(data_inicio, dt.min.time()))
    if data_fim:
        from datetime import datetime as dt
        query = query.filter(Chamado.created_at <= dt.combine(data_fim, dt.max.time()))

    # Ordenação
    _ORDEM = {
        "recente":    Chamado.created_at.desc(),
        "antigo":     Chamado.created_at.asc(),
        "prioridade": Chamado.prioridade.desc(),
        "status":     Chamado.status.asc(),
    }
    query = query.order_by(_ORDEM.get(ordem, Chamado.created_at.desc()))

    # Total antes de paginar
    total = query.count()
    paginas = max(1, -(-total // limit))  # teto da divisão

    # Paginação
    skip = (pagina - 1) * limit
    items = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "pagina": pagina,
        "paginas": paginas,
        "limit": limit,
        "items": items,
    }


# ─── Detalhe ─────────────────────────────────────────────────────────────────

@router.get("/{chamado_id}", response_model=ChamadoResponse)
def obter_chamado(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if current_user.tipo == "cidadao" and chamado.usuario_id != current_user.id:
        raise HTTPException(403, "Sem permissão")
    return chamado


# ─── Criação ─────────────────────────────────────────────────────────────────

@router.post("/", response_model=ChamadoResponse, status_code=status.HTTP_201_CREATED)
async def criar_chamado(
    background_tasks: BackgroundTasks,
    titulo: str = Form(...),
    descricao: str = Form(...),
    endereco: str = Form(...),
    categoria_id: int = Form(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    bairro_id: Optional[int] = Form(None),
    prioridade: Optional[str] = Form("media"),
    foto: Optional[UploadFile] = File(None),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    foto_path = None
    if foto:
        foto_path = await save_upload_file(foto)

    chamado = Chamado(
        titulo=titulo,
        descricao=descricao,
        endereco=endereco,
        latitude=latitude,
        longitude=longitude,
        categoria_id=categoria_id,
        bairro_id=bairro_id,
        prioridade=prioridade,
        foto_antes=foto_path,
        usuario_id=current_user.id,
    )
    db.add(chamado)
    db.flush()  # gera o id

    # Histórico: criação
    registrar_historico(
        db, chamado.id, "criacao",
        None, "aberto",
        usuario_id=current_user.id,
        observacao=f"Chamado aberto: {titulo[:80]}",
    )

    db.commit()
    db.refresh(chamado)

    # Sprint 18: notificação de criação em background
    if current_user.tipo == "cidadao":
        background_tasks.add_task(notificar_criacao, chamado)

    return chamado


# ─── Atualização (legada) ─────────────────────────────────────────────────────

@router.put("/{chamado_id}", response_model=ChamadoResponse)
async def atualizar_chamado(
    chamado_id: int,
    status: Optional[str] = Form(None),
    prioridade: Optional[str] = Form(None),
    responsavel_id: Optional[int] = Form(None),
    foto: Optional[UploadFile] = File(None),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if current_user.tipo == "cidadao":
        raise HTTPException(403, "Sem permissão para atualizar")

    if status and status != chamado.status:
        registrar_historico(db, chamado.id, "status", chamado.status, status, current_user.id)
        chamado.status = status
        if status == "resolvido":
            chamado.data_resolucao = datetime.utcnow()

    if prioridade and prioridade != chamado.prioridade:
        registrar_historico(db, chamado.id, "prioridade", chamado.prioridade, prioridade, current_user.id)
        chamado.prioridade = prioridade

    if responsavel_id and responsavel_id != chamado.responsavel_id:
        registrar_historico(db, chamado.id, "responsavel", chamado.responsavel_id, responsavel_id, current_user.id)
        chamado.responsavel_id = responsavel_id

    if foto:
        chamado.foto_depois = await save_upload_file(foto)

    chamado.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chamado)
    return chamado


# ─── Avaliação ────────────────────────────────────────────────────────────────

@router.post("/{chamado_id}/avaliar", response_model=ChamadoResponse)
def avaliar_chamado(
    chamado_id: int,
    avaliacao_data: ChamadoAvaliar,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if chamado.usuario_id != current_user.id:
        raise HTTPException(403, "Sem permissão")
    if chamado.status != "resolvido":
        raise HTTPException(400, "Apenas chamados resolvidos podem ser avaliados")

    registrar_historico(
        db, chamado.id, "avaliacao",
        chamado.avaliacao, avaliacao_data.avaliacao,
        current_user.id,
        observacao=avaliacao_data.comentario_avaliacao,
    )

    chamado.avaliacao = avaliacao_data.avaliacao
    chamado.comentario_avaliacao = avaliacao_data.comentario_avaliacao
    db.commit()
    db.refresh(chamado)
    return chamado


# ─── PATCH status ─────────────────────────────────────────────────────────────

@router.patch("/{chamado_id}/status", response_model=ChamadoResponse)
def atualizar_status(
    chamado_id: int,
    status_data: StatusUpdate,
    background_tasks: BackgroundTasks,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if current_user.tipo == "cidadao":
        raise HTTPException(403, "Sem permissão")

    status_anterior = chamado.status
    if status_data.status != chamado.status:
        registrar_historico(db, chamado.id, "status", chamado.status, status_data.status, current_user.id)
        chamado.status = status_data.status
        if status_data.status == "resolvido":
            chamado.data_resolucao = datetime.utcnow()

    chamado.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chamado)

    # Sprint 18: notifica cidadão da mudança de status
    background_tasks.add_task(notificar_mudanca_status, chamado, status_anterior)

    return chamado


# ─── PATCH prioridade ─────────────────────────────────────────────────────────

@router.patch("/{chamado_id}/prioridade", response_model=ChamadoResponse)
def atualizar_prioridade(
    chamado_id: int,
    prioridade_data: PrioridadeUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if current_user.tipo not in ["secretaria", "gestor", "admin", "equipe"]:
        raise HTTPException(403, "Sem permissão")

    if prioridade_data.prioridade != chamado.prioridade:
        registrar_historico(db, chamado.id, "prioridade", chamado.prioridade, prioridade_data.prioridade, current_user.id)
        chamado.prioridade = prioridade_data.prioridade

    chamado.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chamado)
    return chamado


# ─── Reclassificar ────────────────────────────────────────────────────────────

@router.patch("/{chamado_id}/reclassificar", response_model=ChamadoResponse)
def reclassificar_chamado(
    chamado_id: int,
    reclassificacao: ReclassificarChamado,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if current_user.tipo not in ["secretaria", "gestor", "admin"]:
        raise HTTPException(403, "Sem permissão para reclassificar")

    obs = (
        f"Serviço {reclassificacao.servico_codigo} — {reclassificacao.servico_nome} | "
        f"Categoria: {reclassificacao.categoria} | SLA: {reclassificacao.sla_horas}h"
    )
    if reclassificacao.prioridade != chamado.prioridade:
        registrar_historico(
            db, chamado.id, "prioridade", chamado.prioridade, reclassificacao.prioridade,
            current_user.id, obs,
        )
    registrar_historico(
        db, chamado.id, "reclassificacao",
        chamado.categoria.nome if chamado.categoria else None,
        reclassificacao.categoria, current_user.id, obs,
    )

    chamado.prioridade = reclassificacao.prioridade
    chamado.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(chamado)
    return chamado


# ─── Histórico do chamado ─────────────────────────────────────────────────────

@router.get("/{chamado_id}/historico")
def historico_chamado(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Timeline completa de alterações do chamado."""
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    if current_user.tipo == "cidadao" and chamado.usuario_id != current_user.id:
        raise HTTPException(403, "Sem permissão")

    historico = (
        db.query(ChamadoHistorico)
        .filter(ChamadoHistorico.chamado_id == chamado_id)
        .order_by(ChamadoHistorico.criado_em.asc())
        .all()
    )
    return [h.to_dict() for h in historico]


# ─── Export CSV ───────────────────────────────────────────────────────────────

@router.get("/export/csv")
def exportar_csv(
    status: Optional[str] = None,
    prioridade: Optional[str] = None,
    bairro_id: Optional[int] = None,
    categoria_id: Optional[int] = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Exporta chamados para CSV — máximo 5.000 registros.
    Apenas gestores, secretarias e admins.
    """
    if current_user.tipo not in ["gestor", "admin", "secretaria"]:
        raise HTTPException(403, "Exportação disponível apenas para gestores e admins")

    query = db.query(Chamado).order_by(Chamado.created_at.desc())
    if status:
        query = query.filter(Chamado.status == status)
    if prioridade:
        query = query.filter(Chamado.prioridade == prioridade)
    if bairro_id:
        query = query.filter(Chamado.bairro_id == bairro_id)
    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)

    chamados = query.limit(5000).all()

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)

    # Cabeçalho
    writer.writerow([
        "Protocolo", "Título", "Status", "Prioridade",
        "Categoria", "Bairro", "Endereço", "Latitude", "Longitude",
        "Avaliação", "Total Votos",
        "Criado em", "Resolvido em",
        "Responsável",
    ])

    # Dados
    for c in chamados:
        dt_criacao   = c.created_at.strftime("%d/%m/%Y %H:%M") if c.created_at else ""
        dt_resolucao = c.data_resolucao.strftime("%d/%m/%Y %H:%M") if c.data_resolucao else ""
        writer.writerow([
            c.protocolo, c.titulo, c.status, c.prioridade,
            c.categoria.nome if c.categoria else "",
            c.bairro.nome if c.bairro else "",
            c.endereco or "", c.latitude or "", c.longitude or "",
            c.avaliacao or "", c.total_votos or 0,
            dt_criacao, dt_resolucao,
            c.responsavel.nome if c.responsavel else "",
        ])

    content = output.getvalue()
    filename = f"chamados_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"

    return Response(
        content=content.encode("utf-8-sig"),  # BOM para Excel reconhecer UTF-8
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ─── Deletar ─────────────────────────────────────────────────────────────────

@router.delete("/{chamado_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_chamado(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.tipo not in ["admin", "gestor"]:
        raise HTTPException(403, "Sem permissão")
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    db.delete(chamado)
    db.commit()
