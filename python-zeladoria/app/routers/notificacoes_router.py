"""
Sprint 15 — Push Notifications com persistência no banco de dados
Substituído o dict em memória (_subscriptions) por tabela push_subscriptions.
Subscriptions agora sobrevivem a restarts e deploys do servidor.
"""
import os, json, logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database.database import get_db
from app.models.usuario import Usuario
from app.models.push_subscription import PushSubscription
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/notificacoes", tags=["Notificações Push"])
logger = logging.getLogger("zelo.push")


class PushSubscriptionSchema(BaseModel):
    endpoint: str
    keys: dict  # {"p256dh": "...", "auth": "..."}


class PushPayload(BaseModel):
    usuario_id: Optional[int] = None  # None = broadcast para todos
    titulo: str
    corpo: str
    url: Optional[str] = "/app"
    icone: Optional[str] = "/static/icons/icon-192.png"


@router.post("/subscribe")
def registrar_subscription(
    sub: PushSubscriptionSchema,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cidadão registra ou atualiza sua subscription Web Push no banco."""
    existente = db.query(PushSubscription).filter_by(usuario_id=current_user.id).first()
    if existente:
        # Upsert: atualiza endpoint + keys se mudaram
        existente.endpoint = sub.endpoint
        existente.keys = sub.keys
        existente.ativa = True
        existente.atualizado_em = datetime.now(timezone.utc)
    else:
        nova = PushSubscription(
            usuario_id=current_user.id,
            endpoint=sub.endpoint,
            keys=sub.keys,
        )
        db.add(nova)

    db.commit()
    total = db.query(PushSubscription).filter_by(ativa=True).count()
    logger.info(f"Push subscription registrada: usuário #{current_user.id}")
    return {"registrado": True, "total_subscriptions": total}


@router.delete("/unsubscribe")
def cancelar_subscription(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Desativa subscription do usuário (mantém registro para auditoria)."""
    sub = db.query(PushSubscription).filter_by(usuario_id=current_user.id).first()
    if sub:
        sub.ativa = False
        db.commit()
    return {"cancelado": True}


@router.post("/enviar")
def enviar_notificacao(
    payload: PushPayload,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Envia push notification para um usuário ou broadcast (admin/gestor/secretaria)."""
    if current_user.tipo not in ("admin", "gestor", "secretaria"):
        raise HTTPException(403, "Sem permissão para enviar notificações")

    if payload.usuario_id is not None:
        subs = db.query(PushSubscription).filter_by(
            usuario_id=payload.usuario_id, ativa=True
        ).all()
    else:
        subs = db.query(PushSubscription).filter_by(ativa=True).all()

    enviadas, falhas = 0, 0
    for sub in subs:
        try:
            _enviar_webpush(
                endpoint=sub.endpoint,
                keys=sub.keys,
                payload=payload,
            )
            enviadas += 1
        except Exception as e:
            falhas += 1
            logger.warning(f"Push falhou para usuário #{sub.usuario_id}: {e}")

    total = db.query(PushSubscription).filter_by(ativa=True).count()
    return {
        "enviadas": enviadas,
        "falhas": falhas,
        "subscriptions_total": total,
    }


def _enviar_webpush(endpoint: str, keys: dict, payload: PushPayload) -> None:
    """
    Envia push via Web Push Protocol (pywebpush).
    Em desenvolvimento (sem VAPID_PRIVATE_KEY): apenas loga.
    """
    VAPID_PRIVATE_KEY  = os.environ.get("VAPID_PRIVATE_KEY", "")
    VAPID_CLAIMS_EMAIL = os.environ.get("VAPID_CLAIMS_EMAIL", "admin@belem.pa.gov.br")

    if not VAPID_PRIVATE_KEY:
        logger.debug(f"[SIMULADO] Push → {endpoint[:50]}: {payload.titulo}")
        return

    try:
        from pywebpush import webpush, WebPushException
        webpush(
            subscription_info={"endpoint": endpoint, "keys": keys},
            data=json.dumps({
                "title": payload.titulo,
                "body": payload.corpo,
                "url": payload.url,
                "icon": payload.icone,
            }),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": f"mailto:{VAPID_CLAIMS_EMAIL}"},
        )
    except Exception as e:
        raise RuntimeError(f"Falha WebPush: {e}")


@router.get("/vapid-public-key")
def vapid_public_key():
    """Retorna a chave pública VAPID para registro de subscriptions no frontend."""
    pub_key = os.environ.get("VAPID_PUBLIC_KEY", "")
    return {
        "vapid_public_key": pub_key or None,
        "configurado": bool(pub_key),
        "instrucao": "Configure VAPID_PUBLIC_KEY e VAPID_PRIVATE_KEY nas variáveis de ambiente.",
    }


@router.get("/status")
def status_notificacoes(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Informa se o usuário atual tem subscription ativa."""
    sub = db.query(PushSubscription).filter_by(
        usuario_id=current_user.id, ativa=True
    ).first()
    total = db.query(PushSubscription).filter_by(ativa=True).count()
    return {
        "subscription_ativa": sub is not None,
        "total_subscriptions_sistema": total,
    }
