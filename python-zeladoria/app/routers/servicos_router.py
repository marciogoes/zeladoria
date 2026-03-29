"""
Rotas API para Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import Optional
from datetime import datetime

from app.database.database import get_db
from app.models_servicos import ServicoSecretaria, PrioridadeServico, StatusServico
from app.schemas.servicos_schemas import (
    ServicoCreate,
    ServicoUpdate,
    ServicoResponse,
    ServicosListResponse,
    ServicoBuscaResult,
    AutocompleteResponse,
    ServicoAtivarDesativar,
    ServicoAlterarStatus,
    ServicoAtualizarSLA,
    DashboardCatalogo,
)

router = APIRouter(prefix="/api/servicos", tags=["Catálogo de Serviços"])


# ============================================================================
# CRUD BÁSICO
# ============================================================================

@router.post("/", response_model=ServicoResponse, status_code=status.HTTP_201_CREATED)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo serviço no catálogo"""
    # Verificar se código já existe
    existe = db.query(ServicoSecretaria).filter_by(codigo=servico.codigo).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um serviço com o código {servico.codigo}"
        )
    
    # Calcular SLA em dias
    sla_dias = servico.sla_horas / 24
    
    # Criar serviço
    db_servico = ServicoSecretaria(
        **servico.model_dump(),
        sla_dias=sla_dias,
        criado_em=datetime.utcnow(),
        atualizado_em=datetime.utcnow()
    )
    
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    
    return db_servico


@router.get("/{servico_id}", response_model=ServicoResponse)
def obter_servico(
    servico_id: int,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um serviço específico"""
    servico = db.query(ServicoSecretaria).filter_by(id=servico_id).first()
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Serviço {servico_id} não encontrado"
        )
    
    return servico


@router.put("/{servico_id}", response_model=ServicoResponse)
def atualizar_servico(
    servico_id: int,
    servico_update: ServicoUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um serviço existente"""
    servico = db.query(ServicoSecretaria).filter_by(id=servico_id).first()
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Serviço {servico_id} não encontrado"
        )
    
    # Atualizar campos
    update_data = servico_update.model_dump(exclude_unset=True)
    
    # Recalcular SLA em dias se necessário
    if 'sla_horas' in update_data:
        update_data['sla_dias'] = update_data['sla_horas'] / 24
    
    update_data['atualizado_em'] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(servico, field, value)
    
    db.commit()
    db.refresh(servico)
    
    return servico


@router.delete("/{servico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_servico(
    servico_id: int,
    db: Session = Depends(get_db)
):
    """Deleta um serviço do catálogo (IRREVERSÍVEL!)"""
    servico = db.query(ServicoSecretaria).filter_by(id=servico_id).first()
    
    if not servico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Serviço {servico_id} não encontrado"
        )
    
    db.delete(servico)
    db.commit()
    
    return None


# ============================================================================
# LISTAGEM E BUSCA
# ============================================================================

@router.get("/", response_model=ServicosListResponse)
def listar_servicos(
    page: int = Query(1, ge=1, description="Página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    secretaria_id: Optional[int] = None,
    categoria: Optional[str] = None,
    subcategoria: Optional[str] = None,
    prioridade: Optional[PrioridadeServico] = None,
    status_servico: Optional[StatusServico] = None,
    apenas_gratuitos: bool = False,
    apenas_online: bool = False,
    busca: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista serviços com filtros e paginação"""
    query = db.query(ServicoSecretaria)
    
    # Aplicar filtros
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    if categoria:
        query = query.filter(ServicoSecretaria.categoria == categoria)
    
    if subcategoria:
        query = query.filter(ServicoSecretaria.subcategoria == subcategoria)
    
    if prioridade:
        query = query.filter(ServicoSecretaria.prioridade == prioridade)
    
    if status_servico:
        query = query.filter(ServicoSecretaria.status == status_servico)
    
    if apenas_gratuitos:
        query = query.filter(ServicoSecretaria.custo == 0)
    
    if apenas_online:
        query = query.filter(ServicoSecretaria.atendimento_online == True)
    
    if busca:
        busca_filter = f"%{busca}%"
        query = query.filter(
            or_(
                ServicoSecretaria.nome.ilike(busca_filter),
                ServicoSecretaria.codigo.ilike(busca_filter),
                ServicoSecretaria.descricao.ilike(busca_filter)
            )
        )
    
    # Contar total
    total = query.count()
    
    # Calcular paginação
    total_pages = (total + page_size - 1) // page_size
    offset = (page - 1) * page_size
    
    # Buscar serviços
    servicos = query.order_by(ServicoSecretaria.codigo).offset(offset).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "servicos": servicos
    }


@router.get("/buscar/avancada", response_model=list[ServicoBuscaResult])
def busca_avancada(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    secretaria_id: Optional[int] = None,
    limite: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Busca avançada com relevância"""
    busca_filter = f"%{q}%"
    
    query = db.query(ServicoSecretaria).filter(
        and_(
            ServicoSecretaria.ativo == True,
            or_(
                ServicoSecretaria.codigo.ilike(busca_filter),
                ServicoSecretaria.nome.ilike(busca_filter),
                ServicoSecretaria.descricao.ilike(busca_filter),
                ServicoSecretaria.categoria.ilike(busca_filter)
            )
        )
    )
    
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    servicos = query.limit(limite).all()
    
    # Calcular relevância
    resultados = []
    for servico in servicos:
        relevancia = 1.0
        q_lower = q.lower()
        
        if q_lower in servico.codigo.lower():
            relevancia += 2.0
        if q_lower in servico.nome.lower():
            relevancia += 1.5
        if servico.descricao and q_lower in servico.descricao.lower():
            relevancia += 0.5
        
        resultado = ServicoBuscaResult.model_validate(servico)
        resultado.relevancia = relevancia
        resultados.append(resultado)
    
    # Ordenar por relevância
    resultados.sort(key=lambda x: x.relevancia, reverse=True)
    
    return resultados


@router.get("/autocomplete", response_model=AutocompleteResponse)
def autocomplete(
    q: str = Query(..., min_length=2),
    secretaria_id: Optional[int] = None,
    limite: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Autocomplete para busca de serviços"""
    busca_filter = f"%{q}%"
    
    query = db.query(ServicoSecretaria).filter(
        and_(
            ServicoSecretaria.ativo == True,
            or_(
                ServicoSecretaria.codigo.ilike(busca_filter),
                ServicoSecretaria.nome.ilike(busca_filter)
            )
        )
    )
    
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    servicos = query.limit(limite).all()
    
    sugestoes = [
        {
            "value": servico.codigo,
            "label": servico.nome,
            "categoria": servico.categoria,
            "sla": servico.sla_em_dias,
            "id": servico.id
        }
        for servico in servicos
    ]
    
    return {"sugestoes": sugestoes}


# ============================================================================
# CATEGORIAS
# ============================================================================

@router.get("/categorias/listar")
def listar_categorias(
    secretaria_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Lista todas as categorias de serviços"""
    query = db.query(
        ServicoSecretaria.categoria,
        func.count(ServicoSecretaria.id).label("total")
    ).filter(ServicoSecretaria.ativo == True)
    
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    categorias = query.group_by(ServicoSecretaria.categoria).all()
    
    return [
        {"categoria": cat, "total_servicos": total}
        for cat, total in categorias
    ]


@router.get("/dashboard", response_model=DashboardCatalogo)
def dashboard_catalogo(
    secretaria_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Dashboard geral do catálogo de serviços"""
    query = db.query(ServicoSecretaria)
    
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    # Cards principais
    total_servicos = query.count()
    servicos_ativos = query.filter(ServicoSecretaria.ativo == True).count()
    
    total_categorias = db.query(func.count(func.distinct(ServicoSecretaria.categoria))).scalar()
    total_secretarias = db.query(func.count(func.distinct(ServicoSecretaria.secretaria_id))).scalar()
    
    # Indicadores
    stats = db.query(
        func.avg(ServicoSecretaria.taxa_cumprimento_sla).label("sla_medio"),
        func.avg(ServicoSecretaria.avaliacao_media).label("avaliacao_media"),
        func.avg(ServicoSecretaria.tempo_medio_atendimento).label("tempo_medio")
    ).filter(ServicoSecretaria.ativo == True).first()
    
    # Distribuição por prioridade
    por_prioridade = {}
    for prioridade in PrioridadeServico:
        count = query.filter(ServicoSecretaria.prioridade == prioridade).count()
        por_prioridade[prioridade.value] = count
    
    # Distribuição por status
    por_status = {}
    for status_enum in StatusServico:
        count = query.filter(ServicoSecretaria.status == status_enum).count()
        por_status[status_enum.value] = count
    
    servicos_gratuitos = query.filter(ServicoSecretaria.custo == 0).count()
    servicos_pagos = query.filter(ServicoSecretaria.custo > 0).count()
    
    # Top categorias
    categorias_top = db.query(
        ServicoSecretaria.categoria,
        func.sum(ServicoSecretaria.total_solicitacoes).label("total")
    ).group_by(ServicoSecretaria.categoria)\
     .order_by(func.sum(ServicoSecretaria.total_solicitacoes).desc())\
     .limit(5).all()
    
    categorias_mais_solicitadas = [
        {"categoria": cat, "total": total or 0}
        for cat, total in categorias_top
    ]
    
    # Top serviços
    melhor_avaliados = query.filter(ServicoSecretaria.avaliacao_media > 0)\
        .order_by(ServicoSecretaria.avaliacao_media.desc())\
        .limit(5).all()
    
    servicos_melhor_avaliados = [
        {"codigo": s.codigo, "nome": s.nome, "avaliacao": s.avaliacao_media}
        for s in melhor_avaliados
    ]
    
    mais_solicitados = query.filter(ServicoSecretaria.total_solicitacoes > 0)\
        .order_by(ServicoSecretaria.total_solicitacoes.desc())\
        .limit(5).all()
    
    servicos_mais_solicitados = [
        {"codigo": s.codigo, "nome": s.nome, "total": s.total_solicitacoes}
        for s in mais_solicitados
    ]
    
    return {
        "total_servicos": total_servicos,
        "servicos_ativos": servicos_ativos,
        "total_categorias": total_categorias,
        "total_secretarias": total_secretarias,
        "taxa_cumprimento_sla_geral": stats.sla_medio or 0,
        "avaliacao_media_geral": stats.avaliacao_media or 0,
        "tempo_medio_atendimento": stats.tempo_medio or 0,
        "por_prioridade": por_prioridade,
        "por_status": por_status,
        "servicos_gratuitos": servicos_gratuitos,
        "servicos_pagos": servicos_pagos,
        "categorias_mais_solicitadas": categorias_mais_solicitadas,
        "servicos_melhor_avaliados": servicos_melhor_avaliados,
        "servicos_mais_solicitados": servicos_mais_solicitados
    }


# ============================================================================
# OPERAÇÕES EM LOTE
# ============================================================================

@router.post("/lote/ativar-desativar")
def ativar_desativar_lote(
    dados: ServicoAtivarDesativar,
    db: Session = Depends(get_db)
):
    """Ativa ou desativa múltiplos serviços"""
    servicos = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.id.in_(dados.servico_ids)
    ).all()
    
    if not servicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum serviço encontrado"
        )
    
    for servico in servicos:
        servico.ativo = dados.ativo
        servico.atualizado_em = datetime.utcnow()
    
    db.commit()
    
    return {
        "mensagem": f"{len(servicos)} serviço(s) {'ativado(s)' if dados.ativo else 'desativado(s)'}",
        "total": len(servicos)
    }


@router.post("/lote/alterar-status")
def alterar_status_lote(
    dados: ServicoAlterarStatus,
    db: Session = Depends(get_db)
):
    """Altera o status de múltiplos serviços"""
    servicos = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.id.in_(dados.servico_ids)
    ).all()
    
    if not servicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum serviço encontrado"
        )
    
    for servico in servicos:
        servico.status = dados.status
        servico.atualizado_em = datetime.utcnow()
    
    db.commit()
    
    return {
        "mensagem": f"{len(servicos)} serviço(s) com status alterado para {dados.status.value}",
        "total": len(servicos)
    }
