"""
Models das Sprints 9-12
Geoespacial + IA + Rastreamento
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base


# ═══════════════════════════════════════════
# SPRINT 9 — Rastreamento GPS de Equipes
# ═══════════════════════════════════════════

class EquipeLocalizacao(Base):
    """Posição em tempo real de cada equipe de campo"""
    __tablename__ = "equipe_localizacoes"

    id          = Column(Integer, primary_key=True, index=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    latitude    = Column(Float, nullable=False)
    longitude   = Column(Float, nullable=False)
    precisao_m  = Column(Float)                  # precisão do GPS em metros
    velocidade  = Column(Float)                  # km/h
    bateria     = Column(Integer)               # % bateria do dispositivo
    em_servico  = Column(Boolean, default=True)
    chamado_id  = Column(Integer, ForeignKey("chamados.id"))  # chamado em atendimento
    registrado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario     = relationship("Usuario")
    chamado     = relationship("Chamado")


class OrdemServico(Base):
    """Ordem de serviço gerada a partir de cluster de chamados"""
    __tablename__ = "ordens_servico"

    id              = Column(Integer, primary_key=True, index=True)
    titulo          = Column(String, nullable=False)
    descricao       = Column(Text)
    centro_lat      = Column(Float)
    centro_lng      = Column(Float)
    raio_metros     = Column(Float, default=100.0)
    chamados_ids    = Column(JSON)       # lista de IDs de chamados agrupados
    total_chamados  = Column(Integer, default=0)
    equipe_id       = Column(Integer, ForeignKey("usuarios.id"))
    status          = Column(String, default="pendente")  # pendente, em_andamento, concluida
    prioridade      = Column(String, default="media")
    criado_em       = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    iniciado_em     = Column(DateTime)
    concluido_em    = Column(DateTime)

    equipe          = relationship("Usuario")


# ═══════════════════════════════════════════
# SPRINT 11 — Triagem IA e Previsão
# ═══════════════════════════════════════════

class LogTriagemIA(Base):
    """Log de triagens automáticas realizadas pela IA"""
    __tablename__ = "logs_triagem_ia"

    id                  = Column(Integer, primary_key=True, index=True)
    chamado_id          = Column(Integer, ForeignKey("chamados.id"))
    texto_entrada       = Column(Text)
    categoria_sugerida  = Column(String)
    prioridade_sugerida = Column(String)
    secretaria_sugerida = Column(String)
    confianca           = Column(Float)        # 0.0 - 1.0
    aceita              = Column(Boolean)      # gestor aceitou a sugestão?
    modelo              = Column(String, default="regras")  # regras | llm
    criado_em           = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    chamado             = relationship("Chamado")


class PrevisaoDemanda(Base):
    """Previsão semanal de chamados por bairro"""
    __tablename__ = "previsoes_demanda"

    id              = Column(Integer, primary_key=True, index=True)
    bairro_id       = Column(Integer, ForeignKey("bairros.id"))
    semana_inicio   = Column(DateTime)
    semana_fim      = Column(DateTime)
    categoria       = Column(String)
    previsao        = Column(Integer)   # chamados esperados
    realizado       = Column(Integer)   # chamados reais (preenchido depois)
    modelo_versao   = Column(String, default="ma4")  # moving average 4 semanas
    gerado_em       = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    bairro          = relationship("Bairro")


class RelatorioMensal(Base):
    """Relatórios mensais gerados automaticamente"""
    __tablename__ = "relatorios_mensais"

    id              = Column(Integer, primary_key=True, index=True)
    ano             = Column(Integer, nullable=False)
    mes             = Column(Integer, nullable=False)
    dados           = Column(JSON)          # snapshot completo dos dados
    arquivo_path    = Column(String)        # caminho do PDF gerado
    gerado_em       = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    gerado_por      = Column(String, default="scheduler")
