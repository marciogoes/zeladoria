from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    icone = Column(String)
    cor = Column(String, default="#667eea")
    sla_horas = Column(Integer, default=72)
    ativo = Column(Boolean, default=True)

    # Relacionamentos
    chamados = relationship("Chamado", back_populates="categoria")
