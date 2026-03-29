"""
Sprint 7 — Scheduler de SLA
Verifica chamados com prazo vencido e escala automaticamente
"""
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger("zelo.sla")

_scheduler = None


def verificar_sla(db_factory):
    """Job: verifica chamados com SLA vencido e gera alertas."""
    from app.models.chamado import Chamado
    from app.models.categoria import Categoria
    from app.utils.auditoria import registrar

    db = db_factory()
    try:
        agora = datetime.utcnow()

        # Busca chamados abertos ou em andamento com SLA configurado
        chamados = (
            db.query(Chamado)
            .filter(Chamado.status.in_(["aberto", "em_andamento"]))
            .all()
        )

        escalados = 0
        for chamado in chamados:
            cat = chamado.categoria
            if not cat or not cat.sla_horas:
                continue

            prazo = chamado.created_at + timedelta(hours=cat.sla_horas)
            if agora > prazo:
                horas_atraso = (agora - prazo).total_seconds() / 3600

                # Escalar prioridade se necessário
                if chamado.prioridade not in ("alta", "critica") and horas_atraso > 24:
                    prioridade_anterior = chamado.prioridade  # captura ANTES de alterar
                    chamado.prioridade = "alta"
                    registrar(db, "Chamado", chamado.id, "sla_escalado",
                              {"prioridade_anterior": prioridade_anterior, "horas_atraso": round(horas_atraso, 1)})
                    escalados += 1

                logger.warning(
                    f"SLA VENCIDO | Protocolo={chamado.protocolo} | "
                    f"Categoria={cat.nome} | Atraso={round(horas_atraso, 1)}h"
                )

        if escalados:
            db.commit()
            logger.info(f"SLA scheduler: {escalados} chamados escalados")
    except Exception as e:
        logger.error(f"Erro no scheduler SLA: {e}")
        db.rollback()
    finally:
        db.close()


def iniciar_scheduler(db_factory):
    global _scheduler
    if _scheduler and _scheduler.running:
        return

    _scheduler = BackgroundScheduler(timezone="America/Belem")
    _scheduler.add_job(
        func=lambda: verificar_sla(db_factory),
        trigger=IntervalTrigger(minutes=30),
        id="verificar_sla",
        replace_existing=True,
        next_run_time=datetime.now(),  # roda imediatamente na primeira vez
    )
    _scheduler.start()
    logger.info("✅ SLA scheduler iniciado — verificação a cada 30 minutos")


def parar_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown()
