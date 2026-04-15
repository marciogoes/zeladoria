"""
Sprint 15 — Scheduler Estendido
Adiciona: relatório mensal automático + backup + limpeza de dados antigos
"""
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger("zelo.scheduler")

_scheduler = None


def verificar_sla(db_factory):
    """Sprint 7: verifica chamados com SLA vencido."""
    from app.models.chamado import Chamado
    from app.utils.auditoria import registrar

    db = db_factory()
    try:
        agora = datetime.now(timezone.utc)
        chamados = db.query(Chamado).filter(
            Chamado.status.in_(["aberto", "em_andamento"])
        ).all()

        escalados = 0
        for c in chamados:
            cat = c.categoria
            if not cat or not cat.sla_horas:
                continue
            prazo = c.created_at + timedelta(hours=cat.sla_horas)
            if agora > prazo:
                horas_atraso = (agora - prazo).total_seconds() / 3600
                if c.prioridade not in ("alta", "critica") and horas_atraso > 24:
                    prioridade_anterior = c.prioridade
                    c.prioridade = "alta"
                    registrar(db, "Chamado", c.id, "sla_escalado",
                              {"prioridade_anterior": prioridade_anterior,
                               "horas_atraso": round(horas_atraso, 1)})
                    escalados += 1
                logger.warning(
                    f"SLA VENCIDO | {c.protocolo} | {cat.nome} | {round(horas_atraso,1)}h atrasado"
                )

        if escalados:
            db.commit()
            logger.info(f"SLA: {escalados} chamados escalados")
    except Exception as e:
        logger.error(f"Erro SLA scheduler: {e}")
        db.rollback()
    finally:
        db.close()


def gerar_relatorio_mensal_auto(db_factory):
    """Sprint 15: gera relatório mensal automaticamente no dia 1."""
    from sqlalchemy import func
    from app.models.chamado import Chamado
    from app.models.categoria import Categoria
    from app.models.bairro import Bairro
    from app.models.sprints_9_12 import RelatorioMensal

    db = db_factory()
    try:
        agora = datetime.now(timezone.utc)
        # Relatório do mês ANTERIOR
        if agora.month == 1:
            mes, ano = 12, agora.year - 1
        else:
            mes, ano = agora.month - 1, agora.year

        # Verifica se já existe
        existente = db.query(RelatorioMensal).filter_by(ano=ano, mes=mes).first()
        if existente:
            logger.info(f"Relatório {mes:02d}/{ano} já existe — pulando")
            return

        inicio = datetime(ano, mes, 1)
        fim = datetime(ano, mes + 1, 1) if mes < 12 else datetime(ano + 1, 1, 1)

        total = db.query(func.count(Chamado.id)).filter(
            Chamado.created_at >= inicio, Chamado.created_at < fim
        ).scalar() or 0

        resolvidos = db.query(func.count(Chamado.id)).filter(
            Chamado.created_at >= inicio, Chamado.created_at < fim,
            Chamado.status == "resolvido",
        ).scalar() or 0

        avaliacao = db.query(func.avg(Chamado.avaliacao)).filter(
            Chamado.created_at >= inicio, Chamado.created_at < fim,
            Chamado.avaliacao.isnot(None),
        ).scalar() or 0

        por_cat = db.query(
            Categoria.nome, func.count(Chamado.id).label("total")
        ).join(Chamado, Chamado.categoria_id == Categoria.id).filter(
            Chamado.created_at >= inicio, Chamado.created_at < fim
        ).group_by(Categoria.nome).order_by(func.count(Chamado.id).desc()).limit(5).all()

        dados = {
            "periodo": f"{mes:02d}/{ano}",
            "total_chamados": total,
            "resolvidos": resolvidos,
            "abertos": total - resolvidos,
            "taxa_resolucao": round(resolvidos / total * 100, 1) if total else 0,
            "avaliacao_media": round(float(avaliacao), 1),
            "top_categorias": [{"categoria": c, "total": t} for c, t in por_cat],
            "gerado_em": agora.isoformat(),
            "gerado_por": "scheduler",
        }

        rel = RelatorioMensal(ano=ano, mes=mes, dados=dados, gerado_por="scheduler")
        db.add(rel)
        db.commit()
        logger.info(f"✅ Relatório {mes:02d}/{ano} gerado automaticamente: {total} chamados, {dados['taxa_resolucao']}% resolvidos")

    except Exception as e:
        logger.error(f"Erro ao gerar relatório mensal: {e}")
        db.rollback()
    finally:
        db.close()


def limpar_localizacoes_antigas(db_factory):
    """Sprint 15: remove localizações GPS com mais de 7 dias (LGPD + espaço)."""
    from app.models.sprints_9_12 import EquipeLocalizacao

    db = db_factory()
    try:
        limite = datetime.now(timezone.utc) - timedelta(days=7)
        deletados = db.query(EquipeLocalizacao).filter(
            EquipeLocalizacao.registrado_em < limite
        ).delete()
        db.commit()
        if deletados:
            logger.info(f"Limpeza GPS: {deletados} localizações antigas removidas")
    except Exception as e:
        logger.error(f"Erro na limpeza de localizações: {e}")
        db.rollback()
    finally:
        db.close()


def backup_banco(db_factory):
    """Sprint 15: gera backup do banco (PostgreSQL via pg_dump ou cópia SQLite)."""
    import os, shutil
    from pathlib import Path

    db_url = os.environ.get("DATABASE_URL", "sqlite:///./zeladoria.db")

    try:
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

        if "sqlite" in db_url:
            src = db_url.replace("sqlite:///./", "").replace("sqlite:///", "")
            dst = backup_dir / f"zeladoria_backup_{ts}.db"
            if os.path.exists(src):
                shutil.copy2(src, dst)
                logger.info(f"✅ Backup SQLite criado: {dst}")
                _limpar_backups_antigos(backup_dir, manter=7)
            else:
                logger.warning(f"Arquivo SQLite não encontrado: {src}")
        else:
            import subprocess
            dst = backup_dir / f"zeladoria_backup_{ts}.sql"
            result = subprocess.run(
                ["pg_dump", db_url, "-f", str(dst)],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                logger.info(f"✅ Backup PostgreSQL criado: {dst}")
                _limpar_backups_antigos(backup_dir, manter=7)
            else:
                logger.error(f"pg_dump falhou: {result.stderr}")

    except Exception as e:
        logger.error(f"Erro no backup: {e}")


def _limpar_backups_antigos(backup_dir, manter: int = 7):
    """Mantém apenas os N backups mais recentes."""
    import os
    from pathlib import Path
    arquivos = sorted(
        Path(backup_dir).glob("zeladoria_backup_*"),
        key=os.path.getmtime,
        reverse=True,
    )
    for arquivo in arquivos[manter:]:
        arquivo.unlink()
        logger.info(f"Backup antigo removido: {arquivo.name}")


def iniciar_scheduler(db_factory):
    global _scheduler
    if _scheduler and _scheduler.running:
        return

    _scheduler = BackgroundScheduler(timezone="America/Belem")

    # SLA — a cada 30 min
    _scheduler.add_job(
        func=lambda: verificar_sla(db_factory),
        trigger=IntervalTrigger(minutes=30),
        id="verificar_sla",
        replace_existing=True,
        next_run_time=datetime.now(),
    )

    # Relatório mensal — todo dia 1 às 02:00
    _scheduler.add_job(
        func=lambda: gerar_relatorio_mensal_auto(db_factory),
        trigger=CronTrigger(day=1, hour=2, minute=0),
        id="relatorio_mensal",
        replace_existing=True,
    )

    # Limpeza GPS — todo dia às 03:00
    _scheduler.add_job(
        func=lambda: limpar_localizacoes_antigas(db_factory),
        trigger=CronTrigger(hour=3, minute=0),
        id="limpar_gps",
        replace_existing=True,
    )

    # Backup — todo dia às 02:30
    _scheduler.add_job(
        func=lambda: backup_banco(db_factory),
        trigger=CronTrigger(hour=2, minute=30),
        id="backup_banco",
        replace_existing=True,
    )

    _scheduler.start()
    logger.info("✅ Scheduler completo iniciado — SLA(30min), Relatório(dia1), Backup(diário), Limpeza GPS(diário)")


def parar_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown()
