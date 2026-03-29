"""
Router para o Catálogo Completo de Serviços
68 serviços distribuídos em 12 secretarias
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text  # ← ADICIONADO!
from typing import Optional, List
from pydantic import BaseModel

from app.database.database import get_db

router = APIRouter(prefix="/api/catalogo", tags=["Catálogo Completo"])


# ============================================================================
# SCHEMAS
# ============================================================================

class ServicoResponse(BaseModel):
    id: int
    codigo: str
    nome: str
    descricao: str
    categoria: str
    subcategoria: Optional[str]
    secretaria_sigla: str
    secretaria_nome: str
    sla_horas: int
    prioridade: str
    status: str
    
    class Config:
        from_attributes = True


class EstatisticasResponse(BaseModel):
    total_servicos: int
    total_secretarias: int
    servicos_emergenciais: int
    sla_medio: float
    por_prioridade: dict
    por_secretaria: List[dict]


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/", response_model=List[ServicoResponse])
def listar_todos_servicos(
    busca: Optional[str] = None,
    secretaria_sigla: Optional[str] = None,
    prioridade: Optional[str] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos os serviços do catálogo com filtros opcionais
    
    - **busca**: Busca por nome, descrição, código ou categoria
    - **secretaria_sigla**: Filtrar por secretaria (ex: SEURB, SESMA)
    - **prioridade**: emergencial, alta, media, baixa, agendavel
    - **categoria**: Filtrar por categoria de serviço
    """
    # Query SQL dinâmica
    query_str = """
        SELECT 
            id, codigo, nome, descricao, categoria, subcategoria,
            secretaria_sigla, secretaria_nome, sla_horas, prioridade, status
        FROM catalogo_servicos
        WHERE status = 'ativo'
    """
    
    params = {}
    
    # Aplicar filtros
    if busca:
        query_str += """ AND (
            nome LIKE :busca OR 
            descricao LIKE :busca OR 
            codigo LIKE :busca OR
            categoria LIKE :busca
        )"""
        params['busca'] = f'%{busca}%'
    
    if secretaria_sigla:
        query_str += " AND secretaria_sigla = :secretaria"
        params['secretaria'] = secretaria_sigla
    
    if prioridade:
        query_str += " AND prioridade = :prioridade"
        params['prioridade'] = prioridade
    
    if categoria:
        query_str += " AND categoria LIKE :categoria"
        params['categoria'] = f'%{categoria}%'
    
    query_str += " ORDER BY codigo"
    
    # Executar query - CORRIGIDO!
    result = db.execute(text(query_str), params)
    servicos = result.fetchall()
    
    return [
        ServicoResponse(
            id=s.id,
            codigo=s.codigo,
            nome=s.nome,
            descricao=s.descricao,
            categoria=s.categoria,
            subcategoria=s.subcategoria,
            secretaria_sigla=s.secretaria_sigla,
            secretaria_nome=s.secretaria_nome,
            sla_horas=s.sla_horas,
            prioridade=s.prioridade,
            status=s.status
        )
        for s in servicos
    ]


@router.get("/servico/{codigo}", response_model=ServicoResponse)
def obter_servico_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """
    Obtém detalhes de um serviço específico pelo código
    
    Exemplo: SEURB-001, SESMA-002, etc.
    """
    query_str = """
        SELECT 
            id, codigo, nome, descricao, categoria, subcategoria,
            secretaria_sigla, secretaria_nome, sla_horas, prioridade, status
        FROM catalogo_servicos
        WHERE codigo = :codigo AND status = 'ativo'
    """
    
    result = db.execute(text(query_str), {'codigo': codigo})
    servico = result.fetchone()
    
    if not servico:
        raise HTTPException(
            status_code=404,
            detail=f"Serviço com código {codigo} não encontrado"
        )
    
    return ServicoResponse(
        id=servico.id,
        codigo=servico.codigo,
        nome=servico.nome,
        descricao=servico.descricao,
        categoria=servico.categoria,
        subcategoria=servico.subcategoria,
        secretaria_sigla=servico.secretaria_sigla,
        secretaria_nome=servico.secretaria_nome,
        sla_horas=servico.sla_horas,
        prioridade=servico.prioridade,
        status=servico.status
    )


@router.get("/estatisticas", response_model=EstatisticasResponse)
def obter_estatisticas(db: Session = Depends(get_db)):
    """
    Retorna estatísticas do catálogo de serviços
    
    - Total de serviços
    - Total de secretarias
    - Serviços emergenciais
    - SLA médio
    - Distribuição por prioridade
    - Distribuição por secretaria
    """
    # Total de serviços
    total_query = text("SELECT COUNT(*) as total FROM catalogo_servicos WHERE status = 'ativo'")
    total = db.execute(total_query).fetchone().total
    
    # Total de secretarias
    secretarias_query = text("SELECT COUNT(DISTINCT secretaria_sigla) as total FROM catalogo_servicos")
    total_secretarias = db.execute(secretarias_query).fetchone().total
    
    # Serviços emergenciais
    emergenciais_query = text("""
        SELECT COUNT(*) as total 
        FROM catalogo_servicos 
        WHERE prioridade = 'emergencial' AND status = 'ativo'
    """)
    emergenciais = db.execute(emergenciais_query).fetchone().total
    
    # SLA médio
    sla_query = text("SELECT AVG(sla_horas) as media FROM catalogo_servicos WHERE status = 'ativo'")
    sla_medio = db.execute(sla_query).fetchone().media or 0
    
    # Por prioridade
    prioridade_query = text("""
        SELECT prioridade, COUNT(*) as total
        FROM catalogo_servicos
        WHERE status = 'ativo'
        GROUP BY prioridade
    """)
    result = db.execute(prioridade_query)
    por_prioridade = {row.prioridade: row.total for row in result}
    
    # Por secretaria
    secretaria_query = text("""
        SELECT 
            secretaria_sigla,
            secretaria_nome,
            COUNT(*) as total_servicos,
            COUNT(CASE WHEN prioridade = 'emergencial' THEN 1 END) as emergenciais
        FROM catalogo_servicos
        WHERE status = 'ativo'
        GROUP BY secretaria_sigla, secretaria_nome
        ORDER BY total_servicos DESC
    """)
    result = db.execute(secretaria_query)
    por_secretaria = [
        {
            "sigla": row.secretaria_sigla,
            "nome": row.secretaria_nome,
            "total": row.total_servicos,
            "emergenciais": row.emergenciais
        }
        for row in result
    ]
    
    return EstatisticasResponse(
        total_servicos=total,
        total_secretarias=total_secretarias,
        servicos_emergenciais=emergenciais,
        sla_medio=round(sla_medio, 2),
        por_prioridade=por_prioridade,
        por_secretaria=por_secretaria
    )


@router.get("/secretarias")
def listar_secretarias(db: Session = Depends(get_db)):
    """Lista todas as secretarias com seus serviços"""
    query_str = text("""
        SELECT 
            secretaria_sigla as sigla,
            secretaria_nome as nome,
            COUNT(*) as total_servicos
        FROM catalogo_servicos
        WHERE status = 'ativo'
        GROUP BY secretaria_sigla, secretaria_nome
        ORDER BY secretaria_sigla
    """)
    
    result = db.execute(query_str)
    
    return [
        {
            "sigla": row.sigla,
            "nome": row.nome,
            "total_servicos": row.total_servicos
        }
        for row in result
    ]


@router.get("/categorias")
def listar_categorias(
    secretaria_sigla: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todas as categorias de serviços"""
    query_str = """
        SELECT DISTINCT categoria, COUNT(*) as total
        FROM catalogo_servicos
        WHERE status = 'ativo'
    """
    
    params = {}
    
    if secretaria_sigla:
        query_str += " AND secretaria_sigla = :secretaria"
        params['secretaria'] = secretaria_sigla
    
    query_str += " GROUP BY categoria ORDER BY categoria"
    
    result = db.execute(text(query_str), params)
    
    return [
        {
            "categoria": row.categoria,
            "total": row.total
        }
        for row in result
    ]


@router.get("/prioridades")
def listar_prioridades(db: Session = Depends(get_db)):
    """Lista todas as prioridades com contagem"""
    query_str = text("""
        SELECT 
            prioridade,
            COUNT(*) as total,
            ROUND(AVG(sla_horas), 2) as sla_medio
        FROM catalogo_servicos
        WHERE status = 'ativo'
        GROUP BY prioridade
        ORDER BY 
            CASE prioridade
                WHEN 'emergencial' THEN 1
                WHEN 'alta' THEN 2
                WHEN 'media' THEN 3
                WHEN 'baixa' THEN 4
                WHEN 'agendavel' THEN 5
            END
    """)
    
    result = db.execute(query_str)
    
    return [
        {
            "prioridade": row.prioridade,
            "total": row.total,
            "sla_medio_horas": row.sla_medio
        }
        for row in result
    ]


@router.get("/buscar")
def buscar_servicos(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    limite: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Busca rápida de serviços
    
    Busca em: nome, descrição, código e categoria
    """
    query_str = text("""
        SELECT 
            id, codigo, nome, descricao, categoria,
            secretaria_sigla, sla_horas, prioridade
        FROM catalogo_servicos
        WHERE status = 'ativo'
        AND (
            nome LIKE :busca OR 
            descricao LIKE :busca OR 
            codigo LIKE :busca OR
            categoria LIKE :busca
        )
        ORDER BY 
            CASE 
                WHEN codigo LIKE :busca THEN 1
                WHEN nome LIKE :busca THEN 2
                ELSE 3
            END,
            codigo
        LIMIT :limite
    """)
    
    result = db.execute(
        query_str, 
        {'busca': f'%{q}%', 'limite': limite}
    )
    
    return [
        {
            "id": row.id,
            "codigo": row.codigo,
            "nome": row.nome,
            "descricao": row.descricao[:100] + "..." if len(row.descricao) > 100 else row.descricao,
            "categoria": row.categoria,
            "secretaria": row.secretaria_sigla,
            "sla_horas": row.sla_horas,
            "prioridade": row.prioridade
        }
        for row in result
    ]
