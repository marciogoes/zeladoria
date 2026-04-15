"""
Sprint 17 — Histórico de Chamados
Trilha imutável de todas as mudanças de status, prioridade e responsável.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base


class ChamadoHistorico(Base):
    """
    Cada linha representa UMA alteração em um chamado.
    Nunca é deletada — fonte de verdade para auditoria e timeline.
    """
    __tablename__ = "chamados_historico"

    id             = Column(Integer, primary_key=True, index=True)
    chamado_id     = Column(Integer, ForeignKey("chamados.id", ondelete="CASCADE"), nullable=False)
    campo          = Column(String(50), nullable=False)   # status | prioridade | responsavel | avaliacao | criacao
    valor_anterior = Column(String(100))
    valor_novo     = Column(String(100), nullable=False)
    observacao     = Column(Text)                          # e.g., "Reclassificado por triagem IA"
    usuario_id     = Column(Integer, ForeignKey("usuarios.id"))
    criado_em      = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relacionamentos (back_populates definido dinamicamente para não circular)
    chamado = relationship("Chamado", foreign_keys=[chamado_id])
    usuario = relationship("Usuario", foreign_keys=[usuario_id])

    def to_dict(self):
        return {
            "id":             self.id,
            "campo":          self.campo,
            "valor_anterior": self.valor_anterior,
            "valor_novo":     self.valor_novo,
            "observacao":     self.observacao,
            "usuario":        self.usuario.nome if self.usuario else "sistema",
            "criado_em":      self.criado_em.isoformat() if self.criado_em else None,
        }


def registrar_historico(
    db,
    chamado_id: int,
    campo: str,
    valor_anterior,
    valor_novo,
    usuario_id: int = None,
    observacao: str = None,
):
    """Helper — registra uma entrada no histórico e faz flush (sem commit)."""
    h = ChamadoHistorico(
        chamado_id=chamado_id,
        campo=campo,
        valor_anterior=str(valor_anterior) if valor_anterior is not None else None,
        valor_novo=str(valor_novo),
        usuario_id=usuario_id,
        observacao=observacao,
    )
    db.add(h)
    db.flush()
    return h
