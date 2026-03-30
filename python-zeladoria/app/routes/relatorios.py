from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.models.usuario import Usuario
from app.utils.auth import require_role

router = APIRouter()


@router.get("/dashboard")
def obter_dashboard(
    current_user: Usuario = Depends(require_role("gestor", "admin", "secretaria", "equipe")),
    db: Session = Depends(get_db),
):
    # Total de chamados
    total_chamados = db.query(func.count(Chamado.id)).scalar() or 0

    # Por status
    por_status = db.query(
        Chamado.status, func.count(Chamado.id).label("total")
    ).group_by(Chamado.status).all()

    # Por prioridade
    por_prioridade = db.query(
        Chamado.prioridade, func.count(Chamado.id).label("total")
    ).group_by(Chamado.prioridade).all()

    # Top 5 categorias
    top_categorias = db.query(
        Categoria.id, Categoria.nome, Categoria.icone, Categoria.cor,
        func.count(Chamado.id).label("total"),
    ).join(Chamado, Chamado.categoria_id == Categoria.id) \
     .group_by(Categoria.id) \
     .order_by(func.count(Chamado.id).desc()) \
     .limit(5).all()

    # Top 5 bairros
    top_bairros = db.query(
        Bairro.id, Bairro.nome, func.count(Chamado.id).label("total"),
    ).join(Chamado, Chamado.bairro_id == Bairro.id) \
     .group_by(Bairro.id) \
     .order_by(func.count(Chamado.id).desc()) \
     .limit(5).all()

    # Chamados recentes
    recentes = db.query(Chamado).order_by(Chamado.created_at.desc()).limit(10).all()

    # Avaliação média
    avaliacao_media = db.query(func.avg(Chamado.avaliacao)) \
        .filter(Chamado.avaliacao.isnot(None)).scalar() or 0

    # ── Sprint 17: Tempo médio de resolução por categoria ─────────────────────
    # Calcula a diferença em segundos entre criação e resolução
    try:
        resolucoes = db.query(
            Categoria.nome,
            Categoria.icone,
            func.count(Chamado.id).label("qtd"),
            # SQLite usa strftime; PostgreSQL usa extract(epoch...) — usamos Python para compatibilidade
        ).join(Chamado, Chamado.categoria_id == Categoria.id) \
         .filter(Chamado.status == "resolvido", Chamado.data_resolucao.isnot(None)) \
         .group_by(Categoria.id) \
         .order_by(func.count(Chamado.id).desc()) \
         .limit(8).all()

        # Para calcular tempo médio: busca os dados em Python (compatível SQLite + PostgreSQL)
        tempo_medio_por_cat = []
        for cat_nome, cat_icone, qtd in resolucoes:
            chamados_resolvidos = db.query(Chamado).join(Categoria, Chamado.categoria_id == Categoria.id) \
                .filter(
                    Categoria.nome == cat_nome,
                    Chamado.status == "resolvido",
                    Chamado.data_resolucao.isnot(None),
                ).limit(200).all()

            if chamados_resolvidos:
                tempos_h = [
                    (c.data_resolucao - c.created_at).total_seconds() / 3600
                    for c in chamados_resolvidos
                    if c.data_resolucao and c.created_at and c.data_resolucao > c.created_at
                ]
                media_h = round(sum(tempos_h) / len(tempos_h), 1) if tempos_h else None
            else:
                media_h = None

            tempo_medio_por_cat.append({
                "categoria": cat_nome,
                "icone": cat_icone,
                "total_resolvidos": qtd,
                "tempo_medio_horas": media_h,
            })

        # Tempo médio geral
        todos_resolvidos = db.query(Chamado).filter(
            Chamado.status == "resolvido",
            Chamado.data_resolucao.isnot(None),
        ).limit(500).all()

        tempos_geral = [
            (c.data_resolucao - c.created_at).total_seconds() / 3600
            for c in todos_resolvidos
            if c.data_resolucao and c.created_at and c.data_resolucao > c.created_at
        ]
        tempo_medio_geral_h = round(sum(tempos_geral) / len(tempos_geral), 1) if tempos_geral else None

    except Exception:
        tempo_medio_por_cat = []
        tempo_medio_geral_h = None

    # Sprint 18: Tendência dos últimos 30 dias (abertura e resolução por dia)
    try:
        agora = datetime.utcnow()
        tendencia = []
        for d in range(29, -1, -1):  # 30 dias, do mais antigo ao mais recente
            dia = agora - timedelta(days=d)
            dia_inicio = dia.replace(hour=0, minute=0, second=0, microsecond=0)
            dia_fim = dia.replace(hour=23, minute=59, second=59, microsecond=999999)
            abertos = db.query(func.count(Chamado.id)).filter(
                Chamado.created_at >= dia_inicio,
                Chamado.created_at <= dia_fim,
            ).scalar() or 0
            resolvidos_dia = db.query(func.count(Chamado.id)).filter(
                Chamado.data_resolucao >= dia_inicio,
                Chamado.data_resolucao <= dia_fim,
                Chamado.status == "resolvido",
            ).scalar() or 0
            tendencia.append({
                "data": dia_inicio.strftime("%d/%m"),
                "data_iso": dia_inicio.strftime("%Y-%m-%d"),
                "abertos": abertos,
                "resolvidos": resolvidos_dia,
            })
    except Exception:
        tendencia = []

    return {
        "total_chamados": total_chamados,
        "por_status": [{"status": s, "total": t} for s, t in por_status],
        "por_prioridade": [{"prioridade": p, "total": t} for p, t in por_prioridade],
        "top_categorias": [
            {
                "categoria": {"id": c.id, "nome": c.nome, "icone": c.icone, "cor": c.cor},
                "total": c.total,
            }
            for c in top_categorias
        ],
        "top_bairros": [
            {"bairro": {"id": b.id, "nome": b.nome}, "total": b.total}
            for b in top_bairros
        ],
        "recentes": [
            {
                "id": r.id,
                "protocolo": r.protocolo,
                "titulo": r.titulo,
                "status": r.status,
                "prioridade": r.prioridade,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "categoria": {"nome": r.categoria.nome, "icone": r.categoria.icone} if r.categoria else None,
                "bairro": {"nome": r.bairro.nome} if r.bairro else None,
            }
            for r in recentes
        ],
        "avaliacao_media": round(float(avaliacao_media), 1),
        # Sprint 17
        "tempo_medio_resolucao_horas": tempo_medio_geral_h,
        "tempo_medio_por_categoria": tempo_medio_por_cat,
        "tendencia_30d": tendencia,  # Sprint 18
    }
