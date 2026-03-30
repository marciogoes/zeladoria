"""
Sprint 15 — Push Notifications, Backup Automático e Scheduler Mensal
"""
import os, json, logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database.database import get_db
from app.models.usuario import Usuario
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/notificacoes", tags=["Notificações Push"])
logger = logging.getLogger("zelo.push")

# Armazena subscriptions em memória (em produção: salvar no banco)
_subscriptions: dict = {}  # usuario_id -> subscription_info


class PushSubscription(BaseModel):
    endpoint: str
    keys: dict  # {"p256dh": "...", "auth": "..."}


class PushPayload(BaseModel):
    usuario_id: Optional[int] = None  # None = broadcast
    titulo: str
    corpo: str
    url: Optional[str] = "/app"
    icone: Optional[str] = "/static/icons/icon-192.png"


@router.post("/subscribe")
def registrar_subscription(
    sub: PushSubscription,
    current_user: Usuario = Depends(get_current_user),
):
    """Cidadão registra subscription Web Push."""
    _subscriptions[current_user.id] = {
        "endpoint": sub.endpoint,
        "keys": sub.keys,
        "usuario_id": current_user.id,
        "registrado_em": datetime.utcnow().isoformat(),
    }
    logger.info(f"Push subscription registrada: usuário #{current_user.id}")
    return {"registrado": True, "total_subscriptions": len(_subscriptions)}


@router.delete("/unsubscribe")
def cancelar_subscription(current_user: Usuario = Depends(get_current_user)):
    """Cancela subscription do usuário."""
    if current_user.id in _subscriptions:
        del _subscriptions[current_user.id]
    return {"cancelado": True}


@router.post("/enviar")
def enviar_notificacao(
    payload: PushPayload,
    current_user: Usuario = Depends(get_current_user),
):
    """
    Envia push notification para um usuário ou broadcast.
    Em produção: usa a Web Push Protocol (pywebpush).
    """
    if current_user.tipo not in ("admin", "gestor", "secretaria"):
        raise HTTPException(403, "Sem permissão para enviar notificações")

    enviadas = 0
    falhas = 0

    alvos = (
        list(_subscriptions.values())
        if payload.usuario_id is None
        else [_subscriptions.get(payload.usuario_id)]
    )

    for sub in alvos:
        if not sub:
            continue
        try:
            _enviar_webpush(sub, payload)
            enviadas += 1
        except Exception as e:
            falhas += 1
            logger.warning(f"Push falhou para endpoint {sub['endpoint'][:40]}: {e}")

    return {
        "enviadas": enviadas,
        "falhas": falhas,
        "subscriptions_total": len(_subscriptions),
    }


def _enviar_webpush(subscription: dict, payload: PushPayload):
    """
    Envia push via Web Push Protocol.
    Em produção: usa pywebpush com VAPID keys.
    Em desenvolvimento: simula o envio.
    """
    VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
    VAPID_CLAIMS_EMAIL = os.environ.get("VAPID_CLAIMS_EMAIL", "admin@belem.pa.gov.br")

    if not VAPID_PRIVATE_KEY:
        # Modo simulação
        logger.debug(f"[SIMULADO] Push para {subscription['endpoint'][:40]}: {payload.titulo}")
        return

    try:
        from pywebpush import webpush, WebPushException
        webpush(
            subscription_info={
                "endpoint": subscription["endpoint"],
                "keys": subscription["keys"],
            },
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
    """Retorna a chave pública VAPID para o frontend registrar subscriptions."""
    pub_key = os.environ.get("VAPID_PUBLIC_KEY", "")
    return {
        "vapid_public_key": pub_key or None,
        "configurado": bool(pub_key),
        "instrucao": "Configure VAPID_PUBLIC_KEY e VAPID_PRIVATE_KEY nas variáveis de ambiente.",
    }


@router.get("/status")
def status_notificacoes(current_user: Usuario = Depends(get_current_user)):
    """Informa se o usuário tem subscription ativa."""
    tem_sub = current_user.id in _subscriptions
    return {
        "subscription_ativa": tem_sub,
        "total_subscriptions_sistema": len(_subscriptions),
    }
