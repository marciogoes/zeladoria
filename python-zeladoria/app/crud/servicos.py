"""
CRUD Operations para Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict
from datetime import datetime, timedelta

from app.models_servicos import ServicoSecretaria, PrioridadeServico, StatusServico
from app.schemas.servicos import (
    ServicoCreate, 
    ServicoUpdate, 
    ServicoFiltros,
    ServicoBusca
)


# ==================== CREATE ====================

def criar_servico(db: Session, servico: ServicoCreate) -> ServicoSecretaria:
    """Cria um novo serviço no catálogo"""
    
    # Calcular SLA em dias automaticamente
    sla_dias = servico.sla_horas / 24
    
    db_servico = ServicoSecretaria(
        **servico.model_dump(),
        sla_dias=sla_dias
    )
    
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico


def criar_servicos_bulk(db: Session, servicos: List[ServicoCreate]) -> List[ServicoSecretaria]:
    """Cria múltiplos serviços de uma vez"""
    servicos_criados = []
    
    for servico_data in servicos:
        try:
            servico = criar_servico(db, servico_data)
            servicos_criados.append(servico)
        except Exception as e:
            print(f"Erro ao criar serviço {servico_data.codigo}: {e}")
            continue
    
    return servicos_criados


# ==================== READ ====================

def get_servico(db: Session, servico_id: int) -> Optional[ServicoSecretaria]:
    """Busca serviço por ID"""
    return db.query(ServicoSecretaria).filter(ServicoSecretaria.id == servico_id).first()


def get_servico_por_codigo(db: Session, codigo: str) -> Optional[ServicoSecretaria]:
    """Busca serviço por código único"""
    return db.query(ServicoSecretaria).filter(ServicoSecretaria.codigo == codigo.upper()).first()


def listar_servicos(
    db: Session,
    filtros: Optional[ServicoFiltros] = None
) -> tuple[List[ServicoSecretaria], int]:
    """
    Lista serviços com filtros e paginação
    Retorna: (lista_servicos, total_count)
    """
    query = db.query(ServicoSecretaria)
    
    # Aplicar filtros
    if filtros:
        if filtros.secretaria_id:
            query = query.filter(ServicoSecretaria.secretaria_id == filtros.secretaria_id)
        
        if filtros.categoria:
            query = query.filter(ServicoSecretaria.categoria == filtros.categoria)
        
        if filtros.subcategoria:
            query = query.filter(ServicoSecretaria.subcategoria == filtros.subcategoria)
        
        if filtros.prioridade:
            query = query.filter(ServicoSecretaria.prioridade == filtros.prioridade)
        
        if filtros.status:
            query = query.filter(ServicoSecretaria.status == filtros.status)
        
        if filtros.ativo is not None:
            query = query.filter(ServicoSecretaria.ativo == filtros.ativo)
        
        if filtros.gratuito is not None:
            if filtros.gratuito:
                query = query.filter(ServicoSecretaria.custo == 0.0)
            else:
                query = query.filter(ServicoSecretaria.custo > 0.0)
        
        if filtros.online:
            query = query.filter(ServicoSecretaria.atendimento_online == True)
    
    # Total antes da paginação
    total = query.count()
    
    # Ordenação
    if filtros and filtros.ordenar_por:
        campo = getattr(ServicoSecretaria, filtros.ordenar_por, None)
        if campo:
            if filtros.ordem == "desc":
                query = query.order_by(desc(campo))
            else:
                query = query.order_by(asc(campo))
    else:
        query = query.order_by(ServicoSecretaria.nome)
    
    # Paginação
    if filtros:
        query = query.offset(filtros.skip).limit(filtros.limit)
    
    servicos = query.all()
    return servicos, total


def buscar_servicos(db: Session, busca: ServicoBusca) -> List[ServicoSecretaria]:
    """Busca serviços por texto em múltiplos campos"""
    query = db.query(ServicoSecretaria)
    
    # Construir condições de busca
    condicoes = []
    termo = f"%{busca.query}%"
    
    if "nome" in busca.campos:
        condicoes.append(ServicoSecretaria.nome.ilike(termo))
    
    if "descricao" in busca.campos:
        condicoes.append(ServicoSecretaria.descricao.ilike(termo))
    
    if "categoria" in busca.campos:
        condicoes.append(ServicoSecretaria.categoria.ilike(termo))
    
    if "subcategoria" in busca.campos:
        condicoes.append(ServicoSecretaria.subcategoria.ilike(termo))
    
    if "codigo" in busca.campos:
        condicoes.append(ServicoSecretaria.codigo.ilike(termo))
    
    # Aplicar OR entre as condições
    if condicoes:
        query = query.filter(or_(*condicoes))
    
    # Aplicar filtros adicionais
    if busca.filtros:
        servicos, _ = listar_servicos(db, busca.filtros)
        return servicos
    
    return query.all()


def get_servicos_por_secretaria(
    db: Session, 
    secretaria_id: int, 
    apenas_ativos: bool = True
) -> List[ServicoSecretaria]:
    """Lista todos os serviços de uma secretaria"""
    query = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.secretaria_id == secretaria_id
    )
    
    if apenas_ativos:
        query = query.filter(
            ServicoSecretaria.ativo == True,
            ServicoSecretaria.status == StatusServico.ATIVO
        )
    
    return query.order_by(ServicoSecretaria.categoria, ServicoSecretaria.nome).all()


def get_categorias(db: Session, secretaria_id: Optional[int] = None) -> List[str]:
    """Lista todas as categorias únicas"""
    query = db.query(ServicoSecretaria.categoria).distinct()
    
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    categorias = query.all()
    return [cat[0] for cat in categorias if cat[0]]


def get_subcategorias(
    db: Session, 
    categoria: str, 
    secretaria_id: Optional[int] = None
) -> List[str]:
    """Lista subcategorias de uma categoria"""
    query = db.query(ServicoSecretaria.subcategoria).filter(
        ServicoSecretaria.categoria == categoria
    ).distinct()
    
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    subcategorias = query.all()
    return [subcat[0] for subcat in subcategorias if subcat[0]]


# ==================== UPDATE ====================

def atualizar_servico(
    db: Session, 
    servico_id: int, 
    servico_update: ServicoUpdate
) -> Optional[ServicoSecretaria]:
    """Atualiza um serviço existente"""
    db_servico = get_servico(db, servico_id)
    
    if not db_servico:
        return None
    
    # Atualizar apenas campos fornecidos
    update_data = servico_update.model_dump(exclude_unset=True)
    
    # Recalcular SLA em dias se sla_horas foi atualizado
    if "sla_horas" in update_data:
        update_data["sla_dias"] = update_data["sla_horas"] / 24
    
    for campo, valor in update_data.items():
        setattr(db_servico, campo, valor)
    
    db_servico.atualizado_em = datetime.utcnow()
    
    db.commit()
    db.refresh(db_servico)
    return db_servico


def atualizar_estatisticas_servico(
    db: Session,
    servico_id: int,
    total_solicitacoes: Optional[int] = None,
    taxa_cumprimento_sla: Optional[float] = None,
    avaliacao_media: Optional[float] = None,
    tempo_medio_atendimento: Optional[int] = None
) -> Optional[ServicoSecretaria]:
    """Atualiza estatísticas de um serviço"""
    db_servico = get_servico(db, servico_id)
    
    if not db_servico:
        return None
    
    if total_solicitacoes is not None:
        db_servico.total_solicitacoes = total_solicitacoes
    
    if taxa_cumprimento_sla is not None:
        db_servico.taxa_cumprimento_sla = round(taxa_cumprimento_sla, 2)
    
    if avaliacao_media is not None:
        db_servico.avaliacao_media = round(avaliacao_media, 2)
    
    if tempo_medio_atendimento is not None:
        db_servico.tempo_medio_atendimento = tempo_medio_atendimento
    
    db.commit()
    db.refresh(db_servico)
    return db_servico


def ativar_desativar_servico(
    db: Session, 
    servico_id: int, 
    ativo: bool
) -> Optional[ServicoSecretaria]:
    """Ativa ou desativa um serviço"""
    db_servico = get_servico(db, servico_id)
    
    if not db_servico:
        return None
    
    db_servico.ativo = ativo
    db_servico.status = StatusServico.ATIVO if ativo else StatusServico.INATIVO
    db_servico.atualizado_em = datetime.utcnow()
    
    db.commit()
    db.refresh(db_servico)
    return db_servico


# ==================== DELETE ====================

def deletar_servico(db: Session, servico_id: int) -> bool:
    """Deleta um serviço (soft delete - marca como inativo)"""
    db_servico = get_servico(db, servico_id)
    
    if not db_servico:
        return False
    
    # Soft delete
    db_servico.ativo = False
    db_servico.status = StatusServico.INATIVO
    db_servico.atualizado_em = datetime.utcnow()
    
    db.commit()
    return True


def deletar_servico_permanente(db: Session, servico_id: int) -> bool:
    """Deleta um serviço permanentemente do banco"""
    db_servico = get_servico(db, servico_id)
    
    if not db_servico:
        return False
    
    db.delete(db_servico)
    db.commit()
    return True


# ==================== ESTATÍSTICAS ====================

def get_estatisticas_servico(db: Session, servico_id: int) -> Optional[Dict]:
    """Retorna estatísticas detalhadas de um serviço"""
    servico = get_servico(db, servico_id)
    
    if not servico:
        return None
    
    # Aqui você pode adicionar queries para buscar dados de chamados relacionados
    # Por enquanto, retorna os dados já existentes no modelo
    
    return {
        "servico_id": servico.id,
        "codigo": servico.codigo,
        "nome": servico.nome,
        "total_solicitacoes": servico.total_solicitacoes,
        "taxa_cumprimento_sla": servico.taxa_cumprimento_sla,
        "avaliacao_media": servico.avaliacao_media,
        "tempo_medio_atendimento": servico.tempo_medio_atendimento,
        "sla_prometido": servico.sla_horas
    }


def get_dashboard_catalogo(db: Session) -> Dict:
    """Retorna dados para dashboard do catálogo"""
    
    # Totais gerais
    total_servicos = db.query(ServicoSecretaria).count()
    servicos_ativos = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.ativo == True
    ).count()
    
    # Categorias únicas
    total_categorias = db.query(ServicoSecretaria.categoria).distinct().count()
    
    # Secretarias únicas
    total_secretarias = db.query(ServicoSecretaria.secretaria_id).distinct().count()
    
    # Por prioridade
    prioridades = {}
    for prioridade in PrioridadeServico:
        count = db.query(ServicoSecretaria).filter(
            ServicoSecretaria.prioridade == prioridade,
            ServicoSecretaria.ativo == True
        ).count()
        prioridades[prioridade.value] = count
    
    # Gratuitos vs Pagos
    servicos_gratuitos = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.custo == 0.0,
        ServicoSecretaria.ativo == True
    ).count()
    
    servicos_pagos = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.custo > 0.0,
        ServicoSecretaria.ativo == True
    ).count()
    
    # Online vs Presencial
    servicos_online = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.atendimento_online == True,
        ServicoSecretaria.ativo == True
    ).count()
    
    servicos_presencial = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.atendimento_presencial == True,
        ServicoSecretaria.ativo == True
    ).count()
    
    # Performance média
    stats = db.query(
        func.avg(ServicoSecretaria.taxa_cumprimento_sla).label('taxa_sla'),
        func.avg(ServicoSecretaria.avaliacao_media).label('avaliacao'),
        func.sum(ServicoSecretaria.total_solicitacoes).label('solicitacoes')
    ).filter(ServicoSecretaria.ativo == True).first()
    
    # Mais solicitados
    mais_solicitados = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.ativo == True
    ).order_by(desc(ServicoSecretaria.total_solicitacoes)).limit(10).all()
    
    # Melhor avaliados
    melhor_avaliados = db.query(ServicoSecretaria).filter(
        ServicoSecretaria.ativo == True,
        ServicoSecretaria.avaliacao_media > 0
    ).order_by(desc(ServicoSecretaria.avaliacao_media)).limit(10).all()
    
    return {
        "total_servicos": total_servicos,
        "servicos_ativos": servicos_ativos,
        "total_categorias": total_categorias,
        "total_secretarias": total_secretarias,
        "emergenciais": prioridades.get("emergencial", 0),
        "alta_prioridade": prioridades.get("alta", 0),
        "media_prioridade": prioridades.get("media", 0),
        "baixa_prioridade": prioridades.get("baixa", 0),
        "agendaveis": prioridades.get("agendavel", 0),
        "servicos_gratuitos": servicos_gratuitos,
        "servicos_pagos": servicos_pagos,
        "servicos_online": servicos_online,
        "servicos_presencial": servicos_presencial,
        "taxa_cumprimento_sla_geral": round(stats.taxa_sla or 0, 2),
        "avaliacao_media_geral": round(stats.avaliacao or 0, 2),
        "total_solicitacoes": int(stats.solicitacoes or 0),
        "servicos_mais_solicitados": mais_solicitados,
        "servicos_melhor_avaliados": melhor_avaliados
    }


def get_estatisticas_por_categoria(db: Session, secretaria_id: Optional[int] = None) -> List[Dict]:
    """Retorna estatísticas agrupadas por categoria"""
    query = db.query(
        ServicoSecretaria.categoria,
        func.count(ServicoSecretaria.id).label('total_servicos'),
        func.sum(ServicoSecretaria.total_solicitacoes).label('total_solicitacoes'),
        func.avg(ServicoSecretaria.taxa_cumprimento_sla).label('taxa_sla'),
        func.avg(ServicoSecretaria.avaliacao_media).label('avaliacao')
    ).filter(ServicoSecretaria.ativo == True)
    
    if secretaria_id:
        query = query.filter(ServicoSecretaria.secretaria_id == secretaria_id)
    
    query = query.group_by(ServicoSecretaria.categoria)
    
    resultados = query.all()
    
    return [
        {
            "categoria": r.categoria,
            "total_servicos": r.total_servicos,
            "total_solicitacoes": int(r.total_solicitacoes or 0),
            "taxa_cumprimento_sla_media": round(r.taxa_sla or 0, 2),
            "avaliacao_media": round(r.avaliacao or 0, 2)
        }
        for r in resultados
    ]
