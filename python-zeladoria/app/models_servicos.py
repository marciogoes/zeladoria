"""
Modelo de Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA

Catálogo de serviços gerenciado por cada secretaria
com SLA (Service Level Agreement) definido
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database.database import Base


class PrioridadeServico(str, enum.Enum):
    """Prioridade do serviço"""
    EMERGENCIAL = "emergencial"    # < 12h
    ALTA = "alta"                   # 12-24h
    MEDIA = "media"                 # 24-72h
    BAIXA = "baixa"                 # > 72h
    AGENDAVEL = "agendavel"         # Pode ser agendado


class StatusServico(str, enum.Enum):
    """Status do serviço no catálogo"""
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    INATIVO = "inativo"


class ServicoSecretaria(Base):
    """
    Catálogo de Serviços de cada Secretaria
    
    Cada secretaria gerencia seu próprio catálogo de serviços
    com SLA (Service Level Agreement) definido
    """
    __tablename__ = "servicos_secretaria"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamento com Secretaria (NULLABLE para permitir criar tabela independentemente)
    secretaria_id = Column(Integer, nullable=True)  # Removida FK temporariamente
    
    # Informações do Serviço
    codigo = Column(String(20), unique=True, nullable=False)  # Ex: SEURB-001
    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    categoria = Column(String(100))  # Categoria principal
    subcategoria = Column(String(100))  # Subcategoria específica
    
    # SLA (Service Level Agreement)
    sla_horas = Column(Integer, nullable=False)  # Tempo em horas
    sla_dias = Column(Float)  # Calculado automaticamente (sla_horas / 24)
    prioridade = Column(SQLEnum(PrioridadeServico), nullable=False)
    
    # Detalhes de Atendimento
    documentos_necessarios = Column(Text)  # Documentos que o cidadão precisa apresentar
    custo = Column(Float, default=0.0)  # Custo do serviço (R$), 0 = gratuito
    tempo_medio_atendimento = Column(Integer)  # Tempo médio real de atendimento (horas)
    
    # Informações Adicionais
    requisitos = Column(Text)  # Requisitos para solicitar o serviço
    observacoes = Column(Text)
    
    # Canais de Atendimento
    atendimento_presencial = Column(Boolean, default=True)
    atendimento_online = Column(Boolean, default=True)
    atendimento_telefone = Column(Boolean, default=True)
    
    # Estatísticas
    total_solicitacoes = Column(Integer, default=0)
    taxa_cumprimento_sla = Column(Float, default=0.0)  # % de cumprimento do SLA
    avaliacao_media = Column(Float, default=0.0)  # Avaliação média (1-5 estrelas)
    
    # Status
    status = Column(SQLEnum(StatusServico), default=StatusServico.ATIVO)
    ativo = Column(Boolean, default=True)
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    criado_por = Column(String(200))  # Usuário que criou
    
    # Relacionamento
    # secretaria = relationship("Secretaria", back_populates="servicos")
    
    def __repr__(self):
        return f"<ServicoSecretaria {self.codigo}: {self.nome} (SLA: {self.sla_horas}h)>"
    
    @property
    def sla_em_dias(self):
        """Retorna SLA em dias formatado"""
        if self.sla_horas < 24:
            return f"{self.sla_horas}h"
        else:
            dias = self.sla_horas / 24
            if dias == int(dias):
                return f"{int(dias)} dia(s)"
            else:
                return f"{dias:.1f} dia(s)"
    
    @property
    def prioridade_label(self):
        """Label da prioridade em português"""
        labels = {
            PrioridadeServico.EMERGENCIAL: "🚨 Emergencial",
            PrioridadeServico.ALTA: "🔴 Alta",
            PrioridadeServico.MEDIA: "🟡 Média",
            PrioridadeServico.BAIXA: "🟢 Baixa",
            PrioridadeServico.AGENDAVEL: "📅 Agendável",
        }
        return labels.get(self.prioridade, self.prioridade.value)
    
    @property
    def custo_formatado(self):
        """Custo formatado"""
        if self.custo == 0:
            return "Gratuito"
        return f"R$ {self.custo:.2f}"


# NOTA: Adicione no modelo Secretaria:
# servicos = relationship("ServicoSecretaria", back_populates="secretaria")

# NOTA: Adicione no modelo Chamado (opcional):
# servico_id = Column(Integer, ForeignKey("servicos_secretaria.id"))
# servico = relationship("ServicoSecretaria")
