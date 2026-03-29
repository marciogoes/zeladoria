from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
import bcrypt


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    telefone = Column(String)
    cpf = Column(String, unique=True)
    tipo = Column(String, default="cidadao")  # cidadao, equipe, gestor, secretaria, admin
    ativo = Column(Boolean, default=True)
    avatar = Column(String)
    
    # Relacionamento com Secretaria (NULLABLE)
    secretaria_id = Column(Integer, nullable=True)

    # Relacionamentos
    chamados = relationship("Chamado", back_populates="usuario", foreign_keys="Chamado.usuario_id")
    chamados_responsavel = relationship("Chamado", back_populates="responsavel", foreign_keys="Chamado.responsavel_id")
    comentarios = relationship("Comentario", back_populates="usuario")

    def verificar_senha(self, senha: str) -> bool:
        """Verifica senha usando bcrypt diretamente"""
        try:
            # Truncar para 72 bytes
            senha_bytes = senha.encode('utf-8')[:72]
            senha_hash = self.senha.encode('utf-8')
            return bcrypt.checkpw(senha_bytes, senha_hash)
        except Exception as e:
            print(f"Erro ao verificar senha: {e}")
            return False

    @staticmethod
    def hash_senha(senha: str) -> str:
        """Hash senha usando bcrypt diretamente"""
        # Truncar para 72 bytes
        senha_bytes = senha.encode('utf-8')[:72]
        # Gerar hash
        hashed = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        # Retornar como string
        return hashed.decode('utf-8')
