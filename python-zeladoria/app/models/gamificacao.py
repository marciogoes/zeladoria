from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


class VotoChamado(Base):
    """Votos de cidadãos em chamados existentes (upvote)"""
    __tablename__ = "votos_chamado"
    __table_args__ = (UniqueConstraint("usuario_id", "chamado_id", name="uq_voto_usuario_chamado"),)

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario")
    chamado = relationship("Chamado", back_populates="votos")


class PontosUsuario(Base):
    """Gamificação — pontuação acumulada por usuário"""
    __tablename__ = "pontos_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, unique=True)
    total_pontos = Column(Integer, default=0)
    chamados_abertos = Column(Integer, default=0)
    votos_dados = Column(Integer, default=0)
    avaliacoes_feitas = Column(Integer, default=0)
    nivel = Column(String, default="iniciante")  # iniciante, colaborador, guardião, zelador, mestre
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuario")


class ConquistaUsuario(Base):
    """Medalhas e conquistas desbloqueadas"""
    __tablename__ = "conquistas_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    conquista = Column(String, nullable=False)   # ex: "primeiro_chamado", "10_votos"
    descricao = Column(String)
    icone = Column(String, default="🏆")
    desbloqueada_em = Column(DateTime, default=datetime.utcnow)
    notificada = Column(Boolean, default=False)

    usuario = relationship("Usuario")
