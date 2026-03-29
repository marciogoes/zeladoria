"""
Utilitário de Auditoria Imutável (Sprint 6)
"""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.sprints_5_8 import RegistroAuditoria


def registrar(
    db: Session,
    entidade: str,
    entidade_id: int,
    acao: str,
    dados: dict = None,
    usuario_id: int = None,
):
    """Cria um bloco de auditoria encadeado ao anterior."""
    # Busca hash do bloco anterior
    ultimo = (
        db.query(RegistroAuditoria)
        .order_by(RegistroAuditoria.id.desc())
        .first()
    )
    hash_anterior = ultimo.hash_bloco if ultimo else "genesis"
    ts = datetime.utcnow()

    hash_bloco = RegistroAuditoria.calcular_hash(
        entidade, entidade_id, acao, dados, hash_anterior, ts
    )

    bloco = RegistroAuditoria(
        entidade=entidade,
        entidade_id=entidade_id,
        acao=acao,
        dados=dados,
        usuario_id=usuario_id,
        hash_bloco=hash_bloco,
        hash_anterior=hash_anterior,
        criado_em=ts,
    )
    db.add(bloco)
    # não commit aqui — deixa para quem chama
    return bloco
