"""
Schemas Pydantic para Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.models_servicos import PrioridadeServico, StatusServico


# ==================== Base Schemas ====================

class ServicoBase(BaseModel):
    """Schema base para serviço"""
    codigo: str = Field(..., min_length=5, max_length=20, description="Código único do serviço (ex: SEURB-001)")
    nome: str = Field(..., min_length=5, max_length=200, description="Nome do serviço")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do serviço")
    categoria: str = Field(..., min_length=3, max_length=100, description="Categoria principal")
    subcategoria: Optional[str] = Field(None, max_length=100, description="Subcategoria específica")
    
    # SLA
    sla_horas: int = Field(..., ge=1, description="SLA em horas (mínimo 1 hora)")
    prioridade: PrioridadeServico = Field(..., description="Prioridade do serviço")
    
    # Detalhes de Atendimento
    documentos_necessarios: Optional[str] = Field(None, description="Documentos necessários")
    custo: float = Field(0.0, ge=0, description="Custo do serviço em R$")
    tempo_medio_atendimento: Optional[int] = Field(None, ge=0, description="Tempo médio real (horas)")
    
    # Informações Adicionais
    requisitos: Optional[str] = Field(None, description="Requisitos para solicitar")
    observacoes: Optional[str] = Field(None, description="Observações importantes")
    
    # Canais de Atendimento
    atendimento_presencial: bool = Field(True, description="Permite atendimento presencial?")
    atendimento_online: bool = Field(True, description="Permite atendimento online?")
    atendimento_telefone: bool = Field(True, description="Permite atendimento telefônico?")
    
    @validator('codigo')
    def validar_codigo(cls, v):
        """Valida formato do código (SECRETARIA-NNN)"""
        if '-' not in v:
            raise ValueError('Código deve estar no formato SECRETARIA-NNN')
        partes = v.split('-')
        if len(partes) != 2:
            raise ValueError('Código deve ter apenas um hífen')
        if not partes[1].isdigit():
            raise ValueError('Parte numérica do código deve conter apenas dígitos')
        return v.upper()
    
    @validator('custo')
    def validar_custo(cls, v):
        """Arredonda custo para 2 casas decimais"""
        return round(v, 2)


class ServicoCreate(ServicoBase):
    """Schema para criar novo serviço"""
    secretaria_id: int = Field(..., gt=0, description="ID da secretaria responsável")
    criado_por: Optional[str] = Field(None, max_length=200, description="Usuário que criou")


class ServicoUpdate(BaseModel):
    """Schema para atualizar serviço existente"""
    nome: Optional[str] = Field(None, min_length=5, max_length=200)
    descricao: Optional[str] = None
    categoria: Optional[str] = Field(None, min_length=3, max_length=100)
    subcategoria: Optional[str] = Field(None, max_length=100)
    
    sla_horas: Optional[int] = Field(None, ge=1)
    prioridade: Optional[PrioridadeServico] = None
    
    documentos_necessarios: Optional[str] = None
    custo: Optional[float] = Field(None, ge=0)
    tempo_medio_atendimento: Optional[int] = Field(None, ge=0)
    
    requisitos: Optional[str] = None
    observacoes: Optional[str] = None
    
    atendimento_presencial: Optional[bool] = None
    atendimento_online: Optional[bool] = None
    atendimento_telefone: Optional[bool] = None
    
    status: Optional[StatusServico] = None
    ativo: Optional[bool] = None


class ServicoResponse(ServicoBase):
    """Schema de resposta com dados completos do serviço"""
    id: int
    secretaria_id: int
    
    # Campos calculados
    sla_dias: Optional[float] = None
    
    # Estatísticas
    total_solicitacoes: int = 0
    taxa_cumprimento_sla: float = 0.0
    avaliacao_media: float = 0.0
    
    # Status
    status: StatusServico
    ativo: bool
    
    # Timestamps
    criado_em: datetime
    atualizado_em: datetime
    criado_por: Optional[str] = None
    
    # Properties formatadas
    sla_em_dias: Optional[str] = None
    prioridade_label: Optional[str] = None
    custo_formatado: Optional[str] = None
    
    class Config:
        from_attributes = True


class ServicoListItem(BaseModel):
    """Schema resumido para listagem de serviços"""
    id: int
    codigo: str
    nome: str
    categoria: str
    subcategoria: Optional[str] = None
    sla_horas: int
    prioridade: PrioridadeServico
    custo: float
    status: StatusServico
    ativo: bool
    
    # Properties
    sla_em_dias: Optional[str] = None
    prioridade_label: Optional[str] = None
    custo_formatado: Optional[str] = None
    
    class Config:
        from_attributes = True


# ==================== Filtros e Busca ====================

class ServicoFiltros(BaseModel):
    """Filtros para busca de serviços"""
    secretaria_id: Optional[int] = Field(None, description="Filtrar por secretaria")
    categoria: Optional[str] = Field(None, description="Filtrar por categoria")
    subcategoria: Optional[str] = Field(None, description="Filtrar por subcategoria")
    prioridade: Optional[PrioridadeServico] = Field(None, description="Filtrar por prioridade")
    status: Optional[StatusServico] = Field(None, description="Filtrar por status")
    ativo: Optional[bool] = Field(None, description="Filtrar por ativo/inativo")
    gratuito: Optional[bool] = Field(None, description="Apenas serviços gratuitos?")
    online: Optional[bool] = Field(None, description="Apenas serviços com atendimento online?")
    
    # Paginação
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(50, ge=1, le=100, description="Número máximo de registros")
    
    # Ordenação
    ordenar_por: Optional[str] = Field("nome", description="Campo para ordenação")
    ordem: Optional[str] = Field("asc", description="Ordem: asc ou desc")


class ServicoBusca(BaseModel):
    """Busca por texto em serviços"""
    query: str = Field(..., min_length=2, description="Termo de busca")
    campos: Optional[List[str]] = Field(
        ["nome", "descricao", "categoria"], 
        description="Campos onde buscar"
    )
    filtros: Optional[ServicoFiltros] = None


# ==================== Estatísticas ====================

class EstatisticasServico(BaseModel):
    """Estatísticas de um serviço específico"""
    servico_id: int
    codigo: str
    nome: str
    
    # Volumes
    total_solicitacoes: int
    solicitacoes_mes_atual: int
    solicitacoes_mes_anterior: int
    
    # SLA
    taxa_cumprimento_sla: float
    tempo_medio_atendimento: Optional[float] = None  # em horas
    sla_prometido: int  # em horas
    
    # Satisfação
    avaliacao_media: float
    total_avaliacoes: int
    
    # Distribuição de status dos chamados
    abertos: int = 0
    em_andamento: int = 0
    resolvidos: int = 0
    cancelados: int = 0


class EstatisticasCategoria(BaseModel):
    """Estatísticas por categoria"""
    categoria: str
    total_servicos: int
    total_solicitacoes: int
    taxa_cumprimento_sla_media: float
    avaliacao_media: float


class EstatisticasSecretaria(BaseModel):
    """Estatísticas por secretaria"""
    secretaria_id: int
    secretaria_nome: str
    total_servicos: int
    total_solicitacoes: int
    taxa_cumprimento_sla_media: float
    avaliacao_media: float
    categorias: List[EstatisticasCategoria] = []


class DashboardCatalogo(BaseModel):
    """Dashboard geral do catálogo"""
    # Resumo Geral
    total_servicos: int
    servicos_ativos: int
    total_categorias: int
    total_secretarias: int
    
    # Por Prioridade
    emergenciais: int = 0
    alta_prioridade: int = 0
    media_prioridade: int = 0
    baixa_prioridade: int = 0
    agendaveis: int = 0
    
    # Atendimento
    servicos_gratuitos: int
    servicos_pagos: int
    servicos_online: int
    servicos_presencial: int
    
    # Performance
    taxa_cumprimento_sla_geral: float
    avaliacao_media_geral: float
    total_solicitacoes: int
    
    # Top 10
    servicos_mais_solicitados: List[ServicoListItem] = []
    servicos_melhor_avaliados: List[ServicoListItem] = []


# ==================== Relatórios ====================

class RelatorioServico(BaseModel):
    """Relatório detalhado de um serviço"""
    servico: ServicoResponse
    estatisticas: EstatisticasServico
    historico_mensal: List[dict] = []  # Últimos 12 meses
    distribuicao_avaliacoes: dict = {}  # 1-5 estrelas


class RelatorioSecretaria(BaseModel):
    """Relatório completo de uma secretaria"""
    secretaria_id: int
    secretaria_nome: str
    periodo: str
    estatisticas: EstatisticasSecretaria
    servicos: List[ServicoResponse]
    graficos: dict = {}


# ==================== Mensagens de Resposta ====================

class Message(BaseModel):
    """Mensagem de resposta genérica"""
    message: str
    detail: Optional[str] = None


class ServicoDeleteResponse(Message):
    """Resposta ao deletar serviço"""
    servico_id: int
    codigo: str


class BulkOperationResponse(Message):
    """Resposta de operações em lote"""
    total_processados: int
    sucesso: int
    falhas: int
    detalhes: List[dict] = []
