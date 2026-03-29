"""
Modelo de Secretarias
Sistema de Zeladoria Urbana - Belém/PA

Este arquivo adiciona o modelo de Secretarias ao sistema
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database.database import Base


class TipoSecretaria(str, enum.Enum):
    """Tipos de secretaria"""
    ADMINISTRACAO = "administracao"
    FINANCAS = "financas"
    INFRAESTRUTURA = "infraestrutura"
    SAUDE = "saude"
    EDUCACAO = "educacao"
    MEIO_AMBIENTE = "meio_ambiente"
    OUTRAS = "outras"
    ORGAO = "orgao"


class Secretaria(Base):
    """
    Modelo de Secretaria Municipal
    
    Representa as secretarias da Prefeitura de Belém que são
    responsáveis pelo atendimento dos chamados
    """
    __tablename__ = "secretarias"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    sigla = Column(String(20), nullable=False, unique=True)
    descricao = Column(Text)
    tipo = Column(SQLEnum(TipoSecretaria), nullable=False)
    
    # Contato
    email = Column(String(200), unique=True)
    telefone = Column(String(20))
    endereco = Column(Text)
    
    # Responsável
    responsavel = Column(String(200))
    cargo_responsavel = Column(String(200))
    
    # Status
    ativa = Column(Boolean, default=True)
    
    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos (serão adicionados quando as outras tabelas forem atualizadas)
    # categorias = relationship("Categoria", back_populates="secretaria")
    # chamados = relationship("Chamado", back_populates="secretaria_responsavel")
    # usuarios = relationship("Usuario", back_populates="secretaria")
    
    def __repr__(self):
        return f"<Secretaria {self.sigla}: {self.nome}>"


# NOTA: Para integração completa, adicione estas colunas nas tabelas existentes:
#
# 1. Na tabela Categoria:
#    secretaria_id = Column(Integer, ForeignKey("secretarias.id"))
#    secretaria = relationship("Secretaria", back_populates="categorias")
#
# 2. Na tabela Chamado:
#    secretaria_responsavel_id = Column(Integer, ForeignKey("secretarias.id"))
#    secretaria_responsavel = relationship("Secretaria", back_populates="chamados")
#
# 3. Na tabela Usuario (para perfil secretaria):
#    secretaria_id = Column(Integer, ForeignKey("secretarias.id"), nullable=True)
#    secretaria = relationship("Secretaria", back_populates="usuarios")
