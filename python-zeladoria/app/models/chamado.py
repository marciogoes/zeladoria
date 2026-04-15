from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database.database import Base

class Chamado(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)
    protocolo = Column(String, unique=True, nullable=False, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    endereco = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    foto_antes = Column(String)
    foto_depois = Column(String)
    status = Column(String, default="aberto")  # aberto, em_andamento, resolvido, cancelado
    prioridade = Column(String, default="media")  # baixa, media, alta, critica
    avaliacao = Column(Integer)
    comentario_avaliacao = Column(Text)
    data_resolucao = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Foreign Keys
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    bairro_id = Column(Integer, ForeignKey("bairros.id"))
    responsavel_id = Column(Integer, ForeignKey("usuarios.id"))

    # Votos (Sprint 3)
    total_votos = Column(Integer, default=0)

    # Secretaria responsável (Sprint 19) — preenchida pela triagem IA ou gestor
    secretaria_id = Column(Integer, ForeignKey("secretarias.id"), nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="chamados", foreign_keys=[usuario_id])
    responsavel = relationship("Usuario", back_populates="chamados_responsavel", foreign_keys=[responsavel_id])
    categoria = relationship("Categoria", back_populates="chamados")
    bairro = relationship("Bairro", back_populates="chamados")
    secretaria = relationship("Secretaria", foreign_keys=[secretaria_id])
    comentarios = relationship("Comentario", back_populates="chamado", cascade="all, delete-orphan")
    votos = relationship("VotoChamado", back_populates="chamado", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.protocolo:
            # UUID v4 truncado: BEL + 10 chars hex → colisão praticamente impossível
            self.protocolo = "BEL" + uuid.uuid4().hex[:10].upper()
