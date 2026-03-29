"""
Modelo de Secretaria
Sistema de Zeladoria Urbana - Belém/PA
"""

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


class Secretaria(Base):
    """
    Secretarias Municipais da Prefeitura de Belém
    """
    __tablename__ = "secretarias"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Informações Básicas
    nome = Column(String(200), nullable=False, unique=True)
    sigla = Column(String(20), nullable=False, unique=True)  # Ex: SEURB, SESAN
    descricao = Column(Text)
    
    # Contato
    telefone = Column(String(20))
    email = Column(String(100))
    site = Column(String(200))
    
    # Endereço
    endereco = Column(String(300))
    bairro = Column(String(100))
    cep = Column(String(10))
    
    # Responsável
    secretario = Column(String(200))  # Nome do secretário
    telefone_secretario = Column(String(20))
    
    # Horário de Funcionamento
    horario_funcionamento = Column(String(200))  # Ex: "Segunda a Sexta, 8h às 14h"
    
    # Cor/Tema (para UI)
    cor_primaria = Column(String(7), default="#0066CC")  # Hex color
    icone = Column(String(50))  # Nome do ícone (FontAwesome, etc)
    
    # Status
    ativo = Column(Boolean, default=True)
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    # usuarios = relationship("Usuario", back_populates="secretaria")
    # servicos = relationship("ServicoSecretaria", back_populates="secretaria")
    
    def __repr__(self):
        return f"<Secretaria {self.sigla}: {self.nome}>"
