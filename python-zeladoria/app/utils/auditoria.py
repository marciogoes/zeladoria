"""
Utility de Auditoria Imutável (Sprint 6)
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.sprints_5_8 import RegistroAuditoria


def registrar(
    db: Session,
    entidade: str,
    entidade_id: int,
    acao: str,
    dados: dict = None,
    usuario_id: int = None,
):
    """
    Cria um bloco de auditoria encadeado ao anterior.
    SELECT ... WITH LOCK garante que dois inserts simultâneos não usem o mesmo hash_anterior,
    preservando a integridade da cadeia blockchain-like.
    """
    # Lock pessimista: bloqueia a leitura do último bloco até o commit
    # → evita race condition onde dois inserts simultâneos leem o mesmo hash_anterior
    try:
        ultimo = (
            db.execute(
                select(RegistroAuditoria)
                .order_by(RegistroAuditoria.id.desc())
                .limit(1)
                .with_for_update(skip_locked=False)
            )
            .scalars()
            .first()
        )
    except Exception:
        # SQLite não suporta FOR UPDATE — fallback silencioso (dev only)
        ultimo = (
            db.query(RegistroAuditoria)
            .order_by(RegistroAuditoria.id.desc())
            .first()
        )

    hash_anterior = ultimo.hash_bloco if ultimo else "genesis"
    ts = datetime.now(timezone.utc)

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
    # sem commit — deixa para quem chama
    return bloco
