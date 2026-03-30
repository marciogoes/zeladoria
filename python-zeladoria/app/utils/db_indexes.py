"""
Sprint 14 — Índices de Performance
Detecta o banco automaticamente e usa a sintaxe correta.
"""
from sqlalchemy import text
import logging

logger = logging.getLogger("zelo.performance")

# Para PostgreSQL (usa CONCURRENTLY fora de transação)
PG_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_chamados_status ON chamados(status)",
    "CREATE INDEX IF NOT EXISTS idx_chamados_prioridade ON chamados(prioridade)",
    "CREATE INDEX IF NOT EXISTS idx_chamados_usuario_id ON chamados(usuario_id)",
    "CREATE INDEX IF NOT EXISTS idx_chamados_bairro_id ON chamados(bairro_id)",
    "CREATE INDEX IF NOT EXISTS idx_chamados_categoria_id ON chamados(categoria_id)",
    "CREATE INDEX IF NOT EXISTS idx_chamados_created_at ON chamados(created_at DESC)",
    "CREATE INDEX IF NOT EXISTS idx_chamados_status_bairro ON chamados(status, bairro_id)",
    "CREATE INDEX IF NOT EXISTS idx_votos_chamado_id ON votos_chamado(chamado_id)",
    "CREATE INDEX IF NOT EXISTS idx_votos_usuario_id ON votos_chamado(usuario_id)",
    "CREATE INDEX IF NOT EXISTS idx_usuarios_tipo ON usuarios(tipo)",
    "CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)",
    "CREATE INDEX IF NOT EXISTS idx_equipe_loc_usuario ON equipe_localizacoes(usuario_id)",
    "CREATE INDEX IF NOT EXISTS idx_equipe_loc_ts ON equipe_localizacoes(registrado_em DESC)",
    "CREATE INDEX IF NOT EXISTS idx_auditoria_entidade ON registros_auditoria(entidade, entidade_id)",
    "CREATE INDEX IF NOT EXISTS idx_auditoria_criado ON registros_auditoria(criado_em DESC)",
    "CREATE INDEX IF NOT EXISTS idx_leituras_sensor_id ON leituras_sensor(sensor_id)",
    "CREATE INDEX IF NOT EXISTS idx_leituras_criado ON leituras_sensor(criado_em DESC)",
    "CREATE INDEX IF NOT EXISTS idx_triagem_criado ON logs_triagem_ia(criado_em DESC)",
]


def criar_indexes(db) -> dict:
    """
    Cria índices de performance.
    Detecta SQLite vs PostgreSQL automaticamente.
    Silencia erros de tabela inexistente (tabelas criadas sob demanda).
    """
    criados = 0
    ignorados = 0
    erros = []

    # Detecta se é SQLite
    engine_name = db.bind.dialect.name if db.bind else "sqlite"
    is_sqlite = engine_name == "sqlite"

    for sql in PG_INDEXES:
        # SQLite não suporta DESC em índices compostos — simplifica
        sql_exec = sql
        if is_sqlite:
            sql_exec = sql.replace(" DESC", "").replace("(status, bairro_id)", "(status)")

        try:
            db.execute(text(sql_exec))
            db.commit()
            criados += 1
        except Exception as e:
            db.rollback()
            err_str = str(e).lower()
            if any(k in err_str for k in ("already exists", "no such table", "no such column")):
                ignorados += 1
            else:
                erros.append({"sql": sql_exec[:60] + "…", "erro": str(e)[:100]})
                logger.debug(f"Índice ignorado: {e}")

    if criados:
        logger.info(f"DB Indexes: {criados} criados, {ignorados} ignorados")
    return {"criados": criados, "ignorados": ignorados, "erros": erros}


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from app.database.database import SessionLocal
    db = SessionLocal()
    r = criar_indexes(db)
    db.close()
    print(f"✅ {r['criados']} criados | ⏭ {r['ignorados']} ignorados | ❌ {len(r['erros'])} erros")
    for e in r["erros"]:
        print(f"  Erro: {e}")
