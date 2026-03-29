"""
Sprint 5 — Integrações Externas
IoT, WhatsApp webhook, API pública, imagens satélite
"""
import os, secrets
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.usuario import Usuario
from app.models.sprints_5_8 import SensorIoT, LeituraSensor
from app.models.bairro import Bairro
from app.models.categoria import Categoria
from app.utils.auth import get_current_user, require_role
from app.utils.auditoria import registrar

router = APIRouter(prefix="/api/integracoes", tags=["Integrações"])


# ─────────────────────────────────────────
# IoT — cadastro de sensores
# ─────────────────────────────────────────
class SensorCreate(BaseModel):
    nome: str
    tipo: str           # alagamento | qualidade_ar | iluminacao | temperatura
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bairro_id: Optional[int] = None
    categoria_id: Optional[int] = None


class LeituraPayload(BaseModel):
    valor: float
    unidade: Optional[str] = None


# Limites de alerta por tipo de sensor
LIMITES_ALERTA = {
    "alagamento":    {"threshold": 30.0,  "titulo": "Alagamento detectado por sensor",    "prioridade": "alta"},
    "qualidade_ar":  {"threshold": 150.0, "titulo": "Qualidade do ar crítica",             "prioridade": "alta"},
    "iluminacao":    {"threshold": 5.0,   "titulo": "Falha na iluminação pública",          "prioridade": "media"},
    "temperatura":   {"threshold": 45.0,  "titulo": "Temperatura elevada na via pública",  "prioridade": "media"},
}


@router.post("/sensores", dependencies=[Depends(require_role("admin", "gestor"))])
def criar_sensor(dados: SensorCreate, db: Session = Depends(get_db)):
    """Cadastra um novo sensor IoT."""
    token = secrets.token_hex(32)
    sensor = SensorIoT(**dados.model_dump(), token=token)
    db.add(sensor)
    db.flush()
    registrar(db, "SensorIoT", sensor.id, "criado", {"nome": sensor.nome, "tipo": sensor.tipo})
    db.commit()
    db.refresh(sensor)
    return {"id": sensor.id, "token": token, "msg": "Sensor cadastrado. Guarde o token — ele não será exibido novamente."}


@router.get("/sensores", dependencies=[Depends(require_role("admin", "gestor", "equipe"))])
def listar_sensores(db: Session = Depends(get_db)):
    sensores = db.query(SensorIoT).filter(SensorIoT.ativo == True).all()
    return [
        {
            "id": s.id, "nome": s.nome, "tipo": s.tipo,
            "latitude": s.latitude, "longitude": s.longitude,
            "bairro": s.bairro.nome if s.bairro else None,
            "ativo": s.ativo,
        }
        for s in sensores
    ]


@router.post("/sensores/leitura")
def receber_leitura(
    payload: LeituraPayload,
    x_sensor_token: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    Endpoint chamado pelo hardware do sensor via HTTP.
    Header obrigatório: X-Sensor-Token
    Se o valor ultrapassar o limite, abre chamado automaticamente.
    """
    sensor = db.query(SensorIoT).filter_by(token=x_sensor_token, ativo=True).first()
    if not sensor:
        raise HTTPException(401, "Token de sensor inválido")

    limite = LIMITES_ALERTA.get(sensor.tipo)
    alerta = bool(limite and payload.valor >= limite["threshold"])

    chamado_id = None
    if alerta:
        # Busca admin/sistema para abrir o chamado
        sistema = db.query(Usuario).filter_by(tipo="admin").first()
        if sistema and sensor.categoria_id:
            chamado = Chamado(
                titulo=limite["titulo"],
                descricao=f"Sensor '{sensor.nome}' registrou {payload.valor} {payload.unidade or ''}. "
                          f"Limite: {limite['threshold']}.",
                endereco=f"Lat {sensor.latitude}, Lon {sensor.longitude}" if sensor.latitude else "Localização do sensor",
                latitude=sensor.latitude,
                longitude=sensor.longitude,
                categoria_id=sensor.categoria_id,
                bairro_id=sensor.bairro_id,
                prioridade=limite["prioridade"],
                usuario_id=sistema.id,
            )
            db.add(chamado)
            db.flush()
            chamado_id = chamado.id

    leitura = LeituraSensor(
        sensor_id=sensor.id,
        valor=payload.valor,
        unidade=payload.unidade,
        alerta=alerta,
        chamado_id=chamado_id,
    )
    db.add(leitura)
    db.commit()

    return {"alerta": alerta, "chamado_id": chamado_id, "leitura_id": leitura.id}


# ─────────────────────────────────────────
# WhatsApp — webhook Meta
# ─────────────────────────────────────────
WA_VERIFY_TOKEN = os.environ.get("WA_VERIFY_TOKEN", "zelo_webhook_token")
WA_ACCESS_TOKEN = os.environ.get("WA_ACCESS_TOKEN", "")


@router.get("/whatsapp/webhook")
def verificar_webhook_whatsapp(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None,
):
    """Verificação do webhook pela Meta (GET)."""
    if hub_mode == "subscribe" and hub_verify_token == WA_VERIFY_TOKEN and hub_challenge:
        return int(hub_challenge)
    raise HTTPException(403, "Token inválido ou challenge ausente")


@router.post("/whatsapp/webhook")
async def receber_mensagem_whatsapp(request: Request, db: Session = Depends(get_db)):
    """
    Recebe mensagens do WhatsApp Business API.
    Fluxo:
      1. Cidadão envia 'NOVO' → inicia cadastro de chamado
      2. Envia descrição → cria chamado com categoria padrão
      3. Envia 'STATUS <protocolo>' → retorna status do chamado
    """
    body = await request.json()
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        msg = entry["messages"][0]
        phone = msg["from"]
        text = msg.get("text", {}).get("body", "").strip().upper()
    except (KeyError, IndexError):
        return {"status": "ignored"}

    resposta = _processar_mensagem_whatsapp(text, phone, db)
    # Em produção: enviar resposta via requests para WA API
    # Por ora retornamos para log
    return {"resposta": resposta, "para": phone}


def _processar_mensagem_whatsapp(text: str, phone: str, db: Session) -> str:
    if text.startswith("STATUS"):
        partes = text.split()
        if len(partes) >= 2:
            protocolo = partes[1]
            chamado = db.query(Chamado).filter_by(protocolo=protocolo).first()
            if chamado:
                STATUS_MAP = {
                    "aberto": "🔵 Aberto — aguardando atendimento",
                    "em_andamento": "🟡 Em andamento — equipe trabalhando",
                    "resolvido": "✅ Resolvido",
                    "cancelado": "❌ Cancelado",
                }
                return (f"*Zelô — Protocolo {protocolo}*\n"
                        f"Título: {chamado.titulo}\n"
                        f"Status: {STATUS_MAP.get(chamado.status, chamado.status)}\n"
                        f"Prioridade: {chamado.prioridade.upper()}")
            return f"Protocolo {protocolo} não encontrado."

    if "NOVO" in text or "ABRIR" in text:
        return ("*Zelô — Novo Chamado*\n"
                "Por favor, descreva o problema em uma mensagem.\n"
                "Exemplo: _Buraco na calçada da Rua Bernal do Couto, 123_\n\n"
                "Para consultar um chamado: STATUS BEL123456789")

    # Qualquer outra mensagem = descrição do problema
    if len(text) > 10:
        # Obter usuário padrão ou criar por telefone
        admin = db.query(Usuario).filter_by(tipo="admin").first()
        cat_default = db.query(Categoria).first()
        if admin and cat_default:
            chamado = Chamado(
                titulo=f"Chamado WhatsApp: {text[:60]}",
                descricao=text,
                endereco="Informado via WhatsApp — confirmar localização",
                categoria_id=cat_default.id,
                prioridade="media",
                usuario_id=admin.id,
            )
            db.add(chamado)
            db.commit()
            return (f"✅ *Chamado registrado!*\n"
                    f"Protocolo: *{chamado.protocolo}*\n"
                    f"Para acompanhar: STATUS {chamado.protocolo}\n\n"
                    f"Acesse também: https://zeladoria-backend-production.up.railway.app/app")

    return ("Olá! Sou o *Zelô*, sistema de zeladoria de Belém 🏛️\n\n"
            "Comandos disponíveis:\n"
            "• *NOVO* — registrar um problema\n"
            "• *STATUS <protocolo>* — consultar chamado\n\n"
            "Exemplo: STATUS BEL1234567890")


# ─────────────────────────────────────────
# Imagens de satélite (via Nominatim + tile preview)
# ─────────────────────────────────────────
@router.get("/satelite/preview")
def preview_satelite(lat: float, lon: float, zoom: int = 17):
    """
    Retorna URL de tile de satélite para visualização no frontend.
    Usa OpenStreetMap (gratuito). Para produção, usar MapBox ou Google Maps.
    """
    # Conversão lat/lon → tile XYZ
    import math
    n = 2 ** zoom
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n)

    return {
        "tile_url": f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png",
        "leaflet_url": f"https://{'{s}'}.tile.openstreetmap.org/{zoom}/{'{x}'}/{'{y}'}.png",
        "lat": lat,
        "lon": lon,
        "zoom": zoom,
        "nota": "Para comparação antes/após, salve screenshots dos chamados ao criar e ao resolver.",
    }
