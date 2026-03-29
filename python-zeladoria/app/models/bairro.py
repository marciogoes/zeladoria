from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

class Bairro(Base):
    __tablename__ = "bairros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    regiao = Column(String)
    ativo = Column(Boolean, default=True)

    # Relacionamentos
    chamados = relationship("Chamado", back_populates="bairro")
