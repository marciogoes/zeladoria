"""
Sprint 13 — SSO com Portal Municipal
Simulação de Single Sign-On com portal cidadão de Belém
Em produção: integrar com o IdP real da Prefeitura (Keycloak/OAuth2)
"""
import os, secrets, hashlib
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.models.usuario import Usuario
from app.utils.auth import create_access_token

router = APIRouter(prefix="/api/sso", tags=["SSO — Portal Municipal"])

# Estado temporário dos code challenges (em produção usar Redis)
_pending_states: dict = {}

# Configurações SSO (variáveis de ambiente em produção)
SSO_CLIENT_ID = os.environ.get("SSO_CLIENT_ID", "zelo-app")
SSO_CLIENT_SECRET = os.environ.get("SSO_CLIENT_SECRET", "")
SSO_PROVIDER_URL = os.environ.get("SSO_PROVIDER_URL", "")  # URL do Keycloak/IdP
SSO_REDIRECT_URI = os.environ.get("SSO_REDIRECT_URI", "https://zeladoria-backend-production.up.railway.app/api/sso/callback")


def _gerar_state() -> str:
    return secrets.token_urlsafe(32)


@router.get("/iniciar")
def iniciar_sso(redirect_after: str = "/app"):
    """
    Inicia o fluxo OAuth2 com o portal municipal.
    Em produção: redireciona para Keycloak/IdP da Prefeitura.
    Em desenvolvimento: retorna URL de simulação.
    """
    state = _gerar_state()
    _pending_states[state] = {
        "criado_em": datetime.utcnow(),
        "redirect_after": redirect_after,
    }

    if SSO_PROVIDER_URL:
        # Produção: redireciona para IdP real
        auth_url = (
            f"{SSO_PROVIDER_URL}/protocol/openid-connect/auth"
            f"?client_id={SSO_CLIENT_ID}"
            f"&response_type=code"
            f"&scope=openid+profile+email"
            f"&redirect_uri={SSO_REDIRECT_URI}"
            f"&state={state}"
        )
        return RedirectResponse(auth_url)

    # Desenvolvimento: retorna URL de simulação
    return {
        "modo": "simulacao",
        "state": state,
        "instrucao": "Em produção, redireciona para o portal cidadão de Belém.",
        "simulacao_url": f"/api/sso/simular-callback?state={state}&codigo=DEMO_CODE",
        "nota": "Configure SSO_PROVIDER_URL para usar IdP real (Keycloak).",
    }


@router.get("/simular-callback")
def simular_callback_sso(
    state: str,
    codigo: str = "DEMO_CODE",
    db: Session = Depends(get_db),
):
    """
    Simula o callback do IdP para demonstração.
    Em produção: este endpoint é substituído pelo /callback real.
    """
    if state not in _pending_states:
        raise HTTPException(400, "State inválido ou expirado")

    info = _pending_states.pop(state)

    # Verifica se expirou (5 min)
    if (datetime.utcnow() - info["criado_em"]).total_seconds() > 300:
        raise HTTPException(400, "Sessão SSO expirada")

    # Simula usuário vindo do portal
    email_simulado = f"cidadao.sso.{hashlib.md5(state.encode()).hexdigest()[:8]}@belem.pa.gov.br"

    # Cria ou recupera usuário
    usuario = db.query(Usuario).filter_by(email=email_simulado).first()
    if not usuario:
        usuario = Usuario(
            nome="Cidadão Portal Belém",
            email=email_simulado,
            senha=Usuario.hash_senha(secrets.token_hex(16)),  # senha aleatória — login só via SSO
            tipo="cidadao",
            ativo=True,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    token = create_access_token(data={"sub": str(usuario.id)})

    # Em produção: redireciona com token no fragment ou via cookie seguro
    redirect = info.get("redirect_after", "/app")
    return RedirectResponse(f"{redirect}?sso_token={token}&sso_nome={usuario.nome}")


@router.get("/callback")
async def callback_sso_real(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    """
    Callback real do OAuth2/OIDC (para quando SSO_PROVIDER_URL estiver configurado).
    Troca o authorization code por token e cria sessão no Zelô.
    """
    if not SSO_PROVIDER_URL:
        raise HTTPException(501, "SSO não configurado. Defina SSO_PROVIDER_URL.")

    if state not in _pending_states:
        raise HTTPException(400, "State inválido ou expirado")

    info = _pending_states.pop(state)

    # Troca code por access_token no IdP
    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{SSO_PROVIDER_URL}/protocol/openid-connect/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": SSO_REDIRECT_URI,
                "client_id": SSO_CLIENT_ID,
                "client_secret": SSO_CLIENT_SECRET,
            },
        )
        if resp.status_code != 200:
            raise HTTPException(401, "Falha na autenticação com portal municipal")

        tokens = resp.json()

        # Busca dados do usuário no IdP
        userinfo = await client.get(
            f"{SSO_PROVIDER_URL}/protocol/openid-connect/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        userdata = userinfo.json()

    email = userdata.get("email", "")
    nome = userdata.get("name", userdata.get("preferred_username", "Cidadão"))

    if not email:
        raise HTTPException(400, "IdP não retornou email do usuário")

    # Cria ou atualiza usuário
    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario:
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=Usuario.hash_senha(secrets.token_hex(16)),
            tipo="cidadao",
            ativo=True,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    else:
        usuario.nome = nome  # Atualiza nome do IdP
        db.commit()

    token = create_access_token(data={"sub": str(usuario.id)})
    redirect = info.get("redirect_after", "/app")
    return RedirectResponse(f"{redirect}?sso_token={token}&sso_nome={nome}")


@router.get("/status")
def status_sso():
    """Informa se o SSO está configurado."""
    return {
        "configurado": bool(SSO_PROVIDER_URL),
        "provider_url": SSO_PROVIDER_URL or None,
        "client_id": SSO_CLIENT_ID,
        "modo": "producao" if SSO_PROVIDER_URL else "simulacao",
        "redirect_uri": SSO_REDIRECT_URI,
    }
