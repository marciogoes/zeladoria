from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Comentario(Base):
    """
    Modelo para comentários/atualizações em chamados
    Permite que equipes e secretarias atualizem o andamento
    """
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)
    chamado_id = Column(Integer, ForeignKey("chamados.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    comentario = Column(Text, nullable=False)
    tipo = Column(String(50), default="atualizacao")  # atualizacao, observacao, resolucao
    visivel_cidadao = Column(Integer, default=1)  # 1 = visível, 0 = apenas interno
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    chamado = relationship("Chamado", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")

    def to_dict(self):
        return {
            "id": self.id,
            "chamado_id": self.chamado_id,
            "usuario_id": self.usuario_id,
            "usuario_nome": self.usuario.nome if self.usuario else "Sistema",
            "usuario_tipo": self.usuario.tipo if self.usuario else "sistema",
            "comentario": self.comentario,
            "tipo": self.tipo,
            "visivel_cidadao": bool(self.visivel_cidadao),
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None
        }
