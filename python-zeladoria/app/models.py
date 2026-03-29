"""
Modelos do Banco de Dados
Sistema de Zeladoria Urbana - Belém/PA
Com suporte a Secretarias Municipais
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base


# ==========================================
# ENUMS
# ==========================================

class TipoUsuario(str, enum.Enum):
    """Tipos de usuário do sistema"""
    CIDADAO = "cidadao"
    EQUIPE = "equipe"
    SECRETARIA = "secretaria"  # NOVO: Perfil para secretarias
    GESTOR = "gestor"
    ADMIN = "admin"


class StatusChamado(str, enum.Enum):
    """Status dos chamados"""
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    AGUARDANDO = "aguardando"
    RESOLVIDO = "resolvido"
    FECHADO = "fechado"
    CANCELADO = "cancelado"


class PrioridadeChamado(str, enum.Enum):
    """Prioridade dos chamados"""
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


# ==========================================
# MODELOS
# ==========================================

class Secretaria(Base):
    """
    Modelo para Secretarias Municipais
    Cada secretaria é responsável por categorias específicas
    """
    __tablename__ = "secretarias"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(20), unique=True, nullable=False)  # Ex: SEMAD, SEURB
    nome = Column(String(200), nullable=False)
    descricao = Column(Text)
    email = Column(String(100))
    telefone = Column(String(20))
    endereco = Column(String(200))
    responsavel = Column(String(100))  # Nome do secretário
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    categorias = relationship("Categoria", back_populates="secretaria")
    usuarios = relationship("Usuario", back_populates="secretaria")
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Secretaria {self.sigla}: {self.nome}>"


class Usuario(Base):
    """Modelo de Usuário"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(200), nullable=False)
    cpf = Column(String(14), unique=True)
    telefone = Column(String(20))
    
    # Tipo de usuário
    tipo = Column(Enum(TipoUsuario), nullable=False, default=TipoUsuario.CIDADAO)
    
    # Secretaria (para usuários tipo SECRETARIA)
    secretaria_id = Column(Integer, ForeignKey("secretarias.id"), nullable=True)
    secretaria = relationship("Secretaria", back_populates="usuarios")
    
    # Status
    ativo = Column(Boolean, default=True)
    
    # Relacionamentos
    chamados = relationship("Chamado", back_populates="cidadao", foreign_keys="Chamado.cidadao_id")
    chamados_atribuidos = relationship("Chamado", back_populates="operador", foreign_keys="Chamado.operador_id")
    avaliacoes = relationship("Avaliacao", back_populates="cidadao")
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    ultimo_acesso = Column(DateTime)

    def __repr__(self):
        return f"<Usuario {self.nome} ({self.tipo})>"


class Categoria(Base):
    """Modelo de Categoria de Chamados"""
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(Text)
    icone = Column(String(50))  # Nome do ícone (Font Awesome, etc)
    cor = Column(String(7))  # Cor em hexadecimal
    
    # Secretaria responsável
    secretaria_id = Column(Integer, ForeignKey("secretarias.id"), nullable=False)
    secretaria = relationship("Secretaria", back_populates="categorias")
    
    # SLA (em horas)
    sla_horas = Column(Integer, default=48)
    
    # Status
    ativa = Column(Boolean, default=True)
    
    # Relacionamentos
    chamados = relationship("Chamado", back_populates="categoria")
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Bairro(Base):
    """Modelo de Bairro"""
    __tablename__ = "bairros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    regiao = Column(String(50))  # Norte, Sul, Leste, Oeste, Centro
    
    # Relacionamentos
    chamados = relationship("Chamado", back_populates="bairro")
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Bairro {self.nome}>"


class Chamado(Base):
    """Modelo de Chamado"""
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)
    protocolo = Column(String(20), unique=True, nullable=False, index=True)
    
    # Informações básicas
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    
    # Relacionamentos
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("Categoria", back_populates="chamados")
    
    bairro_id = Column(Integer, ForeignKey("bairros.id"))
    bairro = relationship("Bairro", back_populates="chamados")
    
    cidadao_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cidadao = relationship("Usuario", back_populates="chamados", foreign_keys=[cidadao_id])
    
    operador_id = Column(Integer, ForeignKey("usuarios.id"))
    operador = relationship("Usuario", back_populates="chamados_atribuidos", foreign_keys=[operador_id])
    
    # Localização
    endereco = Column(String(200))
    referencia = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Status e prioridade
    status = Column(Enum(StatusChamado), nullable=False, default=StatusChamado.ABERTO)
    prioridade = Column(Enum(PrioridadeChamado), default=PrioridadeChamado.MEDIA)
    
    # Anexos
    foto_url = Column(String(500))
    
    # Datas
    data_abertura = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_atribuicao = Column(DateTime)
    data_inicio_atendimento = Column(DateTime)
    data_resolucao = Column(DateTime)
    data_fechamento = Column(DateTime)
    
    # Prazo SLA
    prazo_sla = Column(DateTime)
    
    # Observações internas
    observacoes_internas = Column(Text)
    
    # Relacionamentos
    avaliacoes = relationship("Avaliacao", back_populates="chamado", uselist=False)

    def __repr__(self):
        return f"<Chamado {self.protocolo}: {self.titulo}>"


class Avaliacao(Base):
    """Modelo de Avaliação"""
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamentos
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False, unique=True)
    chamado = relationship("Chamado", back_populates="avaliacoes")
    
    cidadao_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cidadao = relationship("Usuario", back_populates="avaliacoes")
    
    # Avaliação
    nota = Column(Integer, nullable=False)  # 1 a 5
    comentario = Column(Text)
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Avaliacao {self.nota} estrelas - Chamado {self.chamado_id}>"
