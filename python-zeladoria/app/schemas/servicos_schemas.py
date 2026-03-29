"""
Schemas Pydantic para Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models_servicos import PrioridadeServico, StatusServico


# ============================================================================
# SCHEMAS BASE
# ============================================================================

class ServicoBase(BaseModel):
    """Schema base para serviço"""
    codigo: str = Field(..., min_length=5, max_length=20, description="Código único do serviço (ex: SEURB-001)")
    nome: str = Field(..., min_length=5, max_length=200, description="Nome do serviço")
    descricao: Optional[str] = Field(None, description="Descrição detalhada")
    categoria: str = Field(..., min_length=3, max_length=100, description="Categoria principal")
    subcategoria: Optional[str] = Field(None, max_length=100, description="Subcategoria específica")
    
    # SLA
    sla_horas: int = Field(..., ge=1, le=10000, description="Prazo de atendimento em horas")
    prioridade: PrioridadeServico = Field(..., description="Nível de prioridade")
    
    # Detalhes
    documentos_necessarios: Optional[str] = None
    custo: float = Field(default=0.0, ge=0, description="Custo do serviço em R$")
    tempo_medio_atendimento: Optional[int] = Field(None, ge=1, description="Tempo médio real (horas)")
    requisitos: Optional[str] = None
    observacoes: Optional[str] = None
    
    # Canais de Atendimento
    atendimento_presencial: bool = True
    atendimento_online: bool = True
    atendimento_telefone: bool = True
    
    # Status
    status: StatusServico = StatusServico.ATIVO
    ativo: bool = True

    @field_validator('codigo')
    @classmethod
    def validar_codigo(cls, v: str) -> str:
        """Valida formato do código"""
        if not v or '-' not in v:
            raise ValueError('Código deve estar no formato SECRETARIA-000')
        partes = v.split('-')
        if len(partes) != 2:
            raise ValueError('Código deve ter formato SECRETARIA-000')
        if not partes[1].isdigit():
            raise ValueError('Parte numérica do código deve conter apenas dígitos')
        return v.upper()


class ServicoCreate(ServicoBase):
    """Schema para criação de serviço"""
    secretaria_id: int = Field(..., gt=0, description="ID da secretaria responsável")


class ServicoUpdate(BaseModel):
    """Schema para atualização de serviço"""
    nome: Optional[str] = Field(None, min_length=5, max_length=200)
    descricao: Optional[str] = None
    categoria: Optional[str] = Field(None, min_length=3, max_length=100)
    subcategoria: Optional[str] = Field(None, max_length=100)
    
    sla_horas: Optional[int] = Field(None, ge=1, le=10000)
    prioridade: Optional[PrioridadeServico] = None
    
    documentos_necessarios: Optional[str] = None
    custo: Optional[float] = Field(None, ge=0)
    tempo_medio_atendimento: Optional[int] = Field(None, ge=1)
    requisitos: Optional[str] = None
    observacoes: Optional[str] = None
    
    atendimento_presencial: Optional[bool] = None
    atendimento_online: Optional[bool] = None
    atendimento_telefone: Optional[bool] = None
    
    status: Optional[StatusServico] = None
    ativo: Optional[bool] = None


class ServicoResponse(ServicoBase):
    """Schema de resposta com dados do serviço"""
    id: int
    secretaria_id: int
    sla_dias: Optional[float] = None
    
    # Estatísticas
    total_solicitacoes: int = 0
    taxa_cumprimento_sla: float = 0.0
    avaliacao_media: float = 0.0
    
    # Timestamps
    criado_em: datetime
    atualizado_em: datetime
    criado_por: Optional[str] = None
    
    # Properties computadas
    sla_em_dias: str
    prioridade_label: str
    custo_formatado: str

    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS DE LISTAGEM E FILTROS
# ============================================================================

class ServicoListItem(BaseModel):
    """Item resumido para listagens"""
    id: int
    codigo: str
    nome: str
    categoria: str
    subcategoria: Optional[str]
    prioridade: PrioridadeServico
    sla_horas: int
    custo: float
    status: StatusServico
    secretaria_id: int
    
    # Properties
    sla_em_dias: str
    prioridade_label: str
    custo_formatado: str

    class Config:
        from_attributes = True


class ServicosListResponse(BaseModel):
    """Resposta de listagem paginada"""
    total: int
    page: int
    page_size: int
    total_pages: int
    servicos: list[ServicoListItem]


class ServicoFiltros(BaseModel):
    """Filtros para busca de serviços"""
    secretaria_id: Optional[int] = None
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    prioridade: Optional[PrioridadeServico] = None
    status: Optional[StatusServico] = None
    custo_min: Optional[float] = Field(None, ge=0)
    custo_max: Optional[float] = Field(None, ge=0)
    sla_max_horas: Optional[int] = Field(None, ge=1)
    apenas_gratuitos: Optional[bool] = False
    apenas_online: Optional[bool] = False
    busca: Optional[str] = Field(None, description="Busca por nome ou código")


# ============================================================================
# SCHEMAS DE ESTATÍSTICAS
# ============================================================================

class EstatisticasServico(BaseModel):
    """Estatísticas de um serviço"""
    servico_id: int
    codigo: str
    nome: str
    
    total_solicitacoes: int
    solicitacoes_abertas: int
    solicitacoes_em_andamento: int
    solicitacoes_concluidas: int
    solicitacoes_canceladas: int
    
    taxa_cumprimento_sla: float
    tempo_medio_atendimento: float
    avaliacao_media: float
    
    ultimos_30_dias: int
    mes_atual: int


class EstatisticasCategoria(BaseModel):
    """Estatísticas por categoria"""
    categoria: str
    total_servicos: int
    total_solicitacoes: int
    taxa_cumprimento_sla_media: float
    avaliacao_media: float


class EstatisticasSecretaria(BaseModel):
    """Estatísticas da secretaria"""
    secretaria_id: int
    secretaria_nome: str
    
    total_servicos: int
    servicos_ativos: int
    servicos_suspensos: int
    
    total_solicitacoes: int
    taxa_cumprimento_sla: float
    avaliacao_media: float
    
    categorias: list[EstatisticasCategoria]


# ============================================================================
# SCHEMAS DE BUSCA E AUTOCOMPLETE
# ============================================================================

class ServicoBuscaResult(BaseModel):
    """Resultado de busca"""
    id: int
    codigo: str
    nome: str
    descricao: Optional[str]
    categoria: str
    subcategoria: Optional[str]
    sla_em_dias: str
    prioridade_label: str
    custo_formatado: str
    relevancia: float = Field(default=1.0, description="Score de relevância")

    class Config:
        from_attributes = True


class AutocompleteResponse(BaseModel):
    """Resposta para autocomplete"""
    sugestoes: list[dict]  # [{"value": "codigo", "label": "nome", "categoria": "..."}]


# ============================================================================
# SCHEMAS DE OPERAÇÕES EM LOTE
# ============================================================================

class ServicoAtivarDesativar(BaseModel):
    """Ativar/desativar serviços"""
    servico_ids: list[int] = Field(..., min_length=1)
    ativo: bool


class ServicoAlterarStatus(BaseModel):
    """Alterar status de serviços"""
    servico_ids: list[int] = Field(..., min_length=1)
    status: StatusServico


class ServicoAtualizarSLA(BaseModel):
    """Atualizar SLA de serviços"""
    servico_ids: list[int] = Field(..., min_length=1)
    sla_horas: int = Field(..., ge=1, le=10000)
    prioridade: Optional[PrioridadeServico] = None


# ============================================================================
# SCHEMAS DE IMPORTAÇÃO/EXPORTAÇÃO
# ============================================================================

class ServicoImport(BaseModel):
    """Schema para importação CSV/Excel"""
    codigo: str
    nome: str
    categoria: str
    subcategoria: Optional[str] = None
    descricao: Optional[str] = None
    sla_horas: int
    prioridade: str  # Será convertido para enum
    custo: float = 0.0
    documentos_necessarios: Optional[str] = None


class ServicoExport(BaseModel):
    """Schema para exportação"""
    codigo: str
    nome: str
    categoria: str
    subcategoria: Optional[str]
    descricao: Optional[str]
    sla_horas: int
    sla_dias: str
    prioridade: str
    custo: str
    status: str
    total_solicitacoes: int
    taxa_cumprimento_sla: float
    avaliacao_media: float


# ============================================================================
# SCHEMAS DE RELATÓRIOS
# ============================================================================

class RelatorioServicos(BaseModel):
    """Relatório completo de serviços"""
    periodo_inicio: datetime
    periodo_fim: datetime
    
    total_servicos: int
    servicos_ativos: int
    servicos_inativos: int
    
    total_solicitacoes: int
    taxa_cumprimento_sla_geral: float
    avaliacao_media_geral: float
    
    por_secretaria: list[EstatisticasSecretaria]
    por_categoria: list[EstatisticasCategoria]
    top_10_servicos: list[EstatisticasServico]
    servicos_com_problemas: list[ServicoListItem]  # SLA < 70%


class DashboardCatalogo(BaseModel):
    """Dashboard do catálogo de serviços"""
    # Cards principais
    total_servicos: int
    servicos_ativos: int
    total_categorias: int
    total_secretarias: int
    
    # Indicadores
    taxa_cumprimento_sla_geral: float
    avaliacao_media_geral: float
    tempo_medio_atendimento: float
    
    # Distribuição
    por_prioridade: dict[str, int]
    por_status: dict[str, int]
    servicos_gratuitos: int
    servicos_pagos: int
    
    # Tops
    categorias_mais_solicitadas: list[dict]
    servicos_melhor_avaliados: list[dict]
    servicos_mais_solicitados: list[dict]
