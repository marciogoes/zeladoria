"""
Models das Sprints 5-8
Sistema de Zeladoria Urbana - Belém/PA
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib, json
from app.database.database import Base


# ═══════════════════════════════════════════
# SPRINT 5 — IoT
# ═══════════════════════════════════════════
class SensorIoT(Base):
    """Sensor físico cadastrado na cidade"""
    __tablename__ = "sensores_iot"

    id           = Column(Integer, primary_key=True, index=True)
    nome         = Column(String, nullable=False)
    tipo         = Column(String, nullable=False)   # alagamento, qualidade_ar, iluminacao, temperatura
    token        = Column(String, unique=True, nullable=False, index=True)  # auth do sensor
    latitude     = Column(Float)
    longitude    = Column(Float)
    bairro_id    = Column(Integer, ForeignKey("bairros.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    ativo        = Column(Boolean, default=True)
    criado_em    = Column(DateTime, default=datetime.utcnow)

    bairro       = relationship("Bairro")
    categoria    = relationship("Categoria")
    leituras     = relationship("LeituraSensor", back_populates="sensor", cascade="all, delete-orphan")


class LeituraSensor(Base):
    """Leitura enviada pelo sensor"""
    __tablename__ = "leituras_sensor"

    id          = Column(Integer, primary_key=True, index=True)
    sensor_id   = Column(Integer, ForeignKey("sensores_iot.id"), nullable=False)
    valor       = Column(Float, nullable=False)
    unidade     = Column(String)              # mm, ppm, lux, °C …
    alerta      = Column(Boolean, default=False)
    chamado_id  = Column(Integer, ForeignKey("chamados.id"))   # chamado gerado automaticamente
    criado_em   = Column(DateTime, default=datetime.utcnow)

    sensor      = relationship("SensorIoT", back_populates="leituras")
    chamado     = relationship("Chamado")


# ═══════════════════════════════════════════
# SPRINT 6 — Orçamento Participativo
# ═══════════════════════════════════════════
class PropostaOrcamento(Base):
    """Proposta de obra/melhoria para votação cidadã"""
    __tablename__ = "propostas_orcamento"

    id            = Column(Integer, primary_key=True, index=True)
    titulo        = Column(String, nullable=False)
    descricao     = Column(Text)
    categoria     = Column(String)             # infraestrutura, saude, educacao, meio_ambiente …
    bairro_id     = Column(Integer, ForeignKey("bairros.id"))
    custo_estimado= Column(Float)
    autor_id      = Column(Integer, ForeignKey("usuarios.id"))
    status        = Column(String, default="votacao")  # votacao, aprovada, rejeitada, executando, concluida
    total_votos   = Column(Integer, default=0)
    ativa         = Column(Boolean, default=True)
    criado_em     = Column(DateTime, default=datetime.utcnow)
    encerra_em    = Column(DateTime)

    bairro        = relationship("Bairro")
    autor         = relationship("Usuario")
    votos         = relationship("VotoProposta", back_populates="proposta", cascade="all, delete-orphan")


class VotoProposta(Base):
    """Voto de um cidadão numa proposta"""
    __tablename__ = "votos_proposta"
    __table_args__ = (
        UniqueConstraint("usuario_id", "proposta_id", name="uq_voto_proposta"),
    )

    id          = Column(Integer, primary_key=True, index=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    proposta_id = Column(Integer, ForeignKey("propostas_orcamento.id"), nullable=False)
    criado_em   = Column(DateTime, default=datetime.utcnow)

    usuario     = relationship("Usuario")
    proposta    = relationship("PropostaOrcamento", back_populates="votos")


# ═══════════════════════════════════════════
# SPRINT 6 — Auditoria Imutável (Blockchain-like)
# ═══════════════════════════════════════════
class RegistroAuditoria(Base):
    """Trilha de auditoria imutável — cada bloco encadeia o hash do anterior"""
    __tablename__ = "registros_auditoria"

    id            = Column(Integer, primary_key=True, index=True)
    entidade      = Column(String, nullable=False)   # Chamado, Usuario, Proposta …
    entidade_id   = Column(Integer, nullable=False)
    acao          = Column(String, nullable=False)   # criado, status_alterado, votado …
    dados         = Column(JSON)                     # snapshot do estado
    usuario_id    = Column(Integer, ForeignKey("usuarios.id"))
    hash_bloco    = Column(String, nullable=False, unique=True)
    hash_anterior = Column(String)
    criado_em     = Column(DateTime, default=datetime.utcnow)

    usuario       = relationship("Usuario")

    @staticmethod
    def calcular_hash(entidade, entidade_id, acao, dados, hash_anterior, timestamp):
        conteudo = json.dumps({
            "entidade": entidade,
            "entidade_id": entidade_id,
            "acao": acao,
            "dados": dados,
            "hash_anterior": hash_anterior,
            "timestamp": str(timestamp),
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(conteudo.encode()).hexdigest()


# ═══════════════════════════════════════════
# SPRINT 7 — Contratos de Fornecedores
# ═══════════════════════════════════════════
class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id          = Column(Integer, primary_key=True, index=True)
    nome        = Column(String, nullable=False)
    cnpj        = Column(String, unique=True, nullable=False)
    email       = Column(String)
    telefone    = Column(String)
    ativo       = Column(Boolean, default=True)
    criado_em   = Column(DateTime, default=datetime.utcnow)

    contratos   = relationship("ContratoFornecedor", back_populates="fornecedor")


class ContratoFornecedor(Base):
    __tablename__ = "contratos_fornecedor"

    id               = Column(Integer, primary_key=True, index=True)
    fornecedor_id    = Column(Integer, ForeignKey("fornecedores.id"), nullable=False)
    secretaria_id    = Column(Integer, ForeignKey("secretarias.id"))
    numero           = Column(String, unique=True, nullable=False)
    objeto           = Column(Text)
    valor            = Column(Float)
    data_inicio      = Column(DateTime)
    data_fim         = Column(DateTime)
    sla_horas        = Column(Integer, default=48)
    status           = Column(String, default="ativo")  # ativo, suspenso, encerrado
    nota_desempenho  = Column(Float)                    # 0-10, calculado automaticamente
    total_chamados   = Column(Integer, default=0)
    chamados_no_prazo= Column(Integer, default=0)
    criado_em        = Column(DateTime, default=datetime.utcnow)

    fornecedor       = relationship("Fornecedor", back_populates="contratos")
    secretaria       = relationship("Secretaria")


# ═══════════════════════════════════════════
# SPRINT 7 — LGPD
# ═══════════════════════════════════════════
class SolicitacaoLGPD(Base):
    """Solicitações de direito ao esquecimento e anonimização (LGPD)"""
    __tablename__ = "solicitacoes_lgpd"

    id          = Column(Integer, primary_key=True, index=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo        = Column(String, nullable=False)  # exportar, anonimizar, excluir
    status      = Column(String, default="pendente")  # pendente, processando, concluida
    criado_em   = Column(DateTime, default=datetime.utcnow)
    concluido_em= Column(DateTime)

    usuario     = relationship("Usuario")
