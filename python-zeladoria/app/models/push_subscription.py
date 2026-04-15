"""
Sprint 15 — Modelo de Push Subscription persistente
Substitui o dict em memória (_subscriptions) que perdia dados a cada restart.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from datetime import datetime, timezone
from app.database.database import Base


class PushSubscription(Base):
    """
    Armazena a subscription Web Push de cada usuário no banco.
    unique=True em usuario_id garante uma subscription por usuário (upsert no /subscribe).
    """
    __tablename__ = "push_subscriptions"

    id            = Column(Integer, primary_key=True, index=True)
    usuario_id    = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"),
                           nullable=False, unique=True, index=True)
    endpoint      = Column(String, nullable=False)
    keys          = Column(JSON, nullable=False)   # {"p256dh": "...", "auth": "..."}
    ativa         = Column(Boolean, default=True)
    registrado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    atualizado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
