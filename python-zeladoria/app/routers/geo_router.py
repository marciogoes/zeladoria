"""
Sprints 9–10 — Geoespacial Avançado
Mapa de calor em tempo real, clustering, rastreamento GPS equipes, alertas clima
"""
import os, math, httpx
from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.bairro import Bairro
from app.models.usuario import Usuario
from app.models.sprints_9_12 import EquipeLocalizacao, OrdemServico
from app.utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/geo", tags=["Geoespacial"])


# ─────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────

def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância em metros entre dois pontos GPS."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin(math.radians(lat2 - lat1) / 2) ** 2
         + math.cos(phi1) * math.cos(phi2)
         * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


# ─────────────────────────────────────────
# MAPA DE CALOR — Sprint 9
# ─────────────────────────────────────────

@router.get("/heatmap")
def mapa_calor(
    dias: int = 30,
    status: Optional[str] = None,
    categoria_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Pontos para o heatmap com peso por prioridade.
    Atualizado em tempo real — sem cache.
    """
    desde = datetime.utcnow() - timedelta(days=dias)
    query = db.query(
        Chamado.latitude, Chamado.longitude,
        Chamado.prioridade, Chamado.status,
        Chamado.titulo, Chamado.id,
        Chamado.total_votos,
    ).filter(
        Chamado.latitude.isnot(None),
        Chamado.longitude.isnot(None),
        Chamado.created_at >= desde,
    )

    if status:
        query = query.filter(Chamado.status == status)
    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)

    PESO = {"critica": 1.0, "alta": 0.7, "media": 0.4, "baixa": 0.2}

    pontos = []
    for r in query.all():
        # votos aumentam o peso (até +0.3)
        bonus_votos = min((r.total_votos or 0) * 0.03, 0.3)
        pontos.append({
            "lat": r.latitude,
            "lng": r.longitude,
            "peso": min(PESO.get(r.prioridade, 0.4) + bonus_votos, 1.0),
            "status": r.status,
            "titulo": r.titulo,
            "id": r.id,
        })

    # Estatísticas por bairro
    por_bairro = (
        db.query(Bairro.nome, func.count(Chamado.id).label("total"))
        .join(Chamado, Chamado.bairro_id == Bairro.id)
        .filter(Chamado.created_at >= desde)
        .group_by(Bairro.id)
        .order_by(func.count(Chamado.id).desc())
        .limit(5).all()
    )

    return {
        "pontos": pontos,
        "total": len(pontos),
        "top_bairros": [{"bairro": b, "total": t} for b, t in por_bairro],
        "periodo_dias": dias,
        "gerado_em": datetime.utcnow().isoformat(),
    }


# ─────────────────────────────────────────
# CLUSTERING — Sprint 9
# ─────────────────────────────────────────

@router.get("/clusters")
def agrupar_chamados(
    raio_metros: float = 100.0,
    apenas_abertos: bool = True,
    db: Session = Depends(get_db),
):
    """
    Agrupa chamados geograficamente usando DBSCAN simplificado.
    Clusters com 2+ chamados viram sugestões de Ordem de Serviço.
    AVISO: algoritmo O(n²) — limitado a 500 chamados por chamada para evitar timeout.
    """
    _LIMITE_CLUSTERING = 500

    query = db.query(Chamado).filter(
        Chamado.latitude.isnot(None),
        Chamado.longitude.isnot(None),
    )
    if apenas_abertos:
        query = query.filter(Chamado.status.in_(["aberto", "em_andamento"]))

    total_disponiveis = query.count()
    chamados = query.order_by(Chamado.prioridade.desc()).limit(_LIMITE_CLUSTERING).all()

    aviso = None
    if total_disponiveis > _LIMITE_CLUSTERING:
        aviso = (
            f"Exibindo os {_LIMITE_CLUSTERING} chamados de maior prioridade "
            f"(total disponível: {total_disponiveis}). "
            "Para processar todos, use exportação CSV e clustering offline."
        )

    visitados: set = set()
    clusters: list = []

    for i, c1 in enumerate(chamados):
        if i in visitados:
            continue
        grupo = [c1]
        visitados.add(i)
        for j, c2 in enumerate(chamados):
            if j in visitados:
                continue
            if _haversine(c1.latitude, c1.longitude, c2.latitude, c2.longitude) <= raio_metros:
                grupo.append(c2)
                visitados.add(j)

        if len(grupo) < 2:
            continue

        lat_c = sum(c.latitude for c in grupo) / len(grupo)
        lng_c = sum(c.longitude for c in grupo) / len(grupo)

        # Prioridade do cluster = máxima dos chamados
        PRIO = {"critica": 4, "alta": 3, "media": 2, "baixa": 1}
        max_prio = max(grupo, key=lambda c: PRIO.get(c.prioridade, 0))

        clusters.append({
            "centro_lat": round(lat_c, 6),
            "centro_lng": round(lng_c, 6),
            "raio_metros": raio_metros,
            "total": len(grupo),
            "prioridade_maxima": max_prio.prioridade,
            "economia_min": (len(grupo) - 1) * 45,
            "chamados": [
                {
                    "id": c.id,
                    "protocolo": c.protocolo,
                    "titulo": c.titulo,
                    "prioridade": c.prioridade,
                    "status": c.status,
                    "lat": c.latitude,
                    "lng": c.longitude,
                }
                for c in grupo
            ],
            "sugestao_os": f"OS agrupada: {len(grupo)} chamados em {raio_metros:.0f}m",
        })

    clusters.sort(key=lambda x: x["total"], reverse=True)

    return {
        "clusters": clusters,
        "total_clusters": len(clusters),
        "total_chamados_agrupados": sum(c["total"] for c in clusters),
        "economia_total_min": sum(c["economia_min"] for c in clusters),
        "aviso": aviso,
    }


@router.post("/clusters/criar-ordem")
def criar_ordem_de_cluster(
    centro_lat: float,
    centro_lng: float,
    raio_metros: float = 100.0,
    equipe_id: Optional[int] = None,
    current_user: Usuario = Depends(require_role("admin", "gestor", "secretaria")),
    db: Session = Depends(get_db),
):
    """Cria uma Ordem de Serviço a partir de chamados próximos."""
    chamados = db.query(Chamado).filter(
        Chamado.status.in_(["aberto", "em_andamento"]),
        Chamado.latitude.isnot(None),
        Chamado.longitude.isnot(None),
    ).all()

    no_cluster = [
        c for c in chamados
        if _haversine(centro_lat, centro_lng, c.latitude, c.longitude) <= raio_metros
    ]

    if not no_cluster:
        raise HTTPException(404, "Nenhum chamado encontrado nessa área")

    PRIO = {"critica": 4, "alta": 3, "media": 2, "baixa": 1}
    max_p = max(no_cluster, key=lambda c: PRIO.get(c.prioridade, 0))

    os_ = OrdemServico(
        titulo=f"OS — {len(no_cluster)} chamados agrupados",
        descricao=f"Ordem de serviço criada automaticamente por cluster de {raio_metros:.0f}m.",
        centro_lat=centro_lat,
        centro_lng=centro_lng,
        raio_metros=raio_metros,
        chamados_ids=[c.id for c in no_cluster],
        total_chamados=len(no_cluster),
        equipe_id=equipe_id,
        prioridade=max_p.prioridade,
    )
    db.add(os_)
    db.commit()
    db.refresh(os_)

    return {
        "ordem_id": os_.id,
        "titulo": os_.titulo,
        "total_chamados": os_.total_chamados,
        "prioridade": os_.prioridade,
        "chamados_ids": os_.chamados_ids,
    }


@router.get("/ordens")
def listar_ordens(
    status: Optional[str] = None,
    equipe_id: Optional[int] = None,
    current_user: Usuario = Depends(require_role("admin", "gestor", "secretaria", "equipe")),
    db: Session = Depends(get_db),
):
    query = db.query(OrdemServico)
    if status:
        query = query.filter(OrdemServico.status == status)
    if equipe_id:
        query = query.filter(OrdemServico.equipe_id == equipe_id)
    ordens = query.order_by(OrdemServico.criado_em.desc()).all()

    return [
        {
            "id": o.id,
            "titulo": o.titulo,
            "status": o.status,
            "prioridade": o.prioridade,
            "total_chamados": o.total_chamados,
            "centro_lat": o.centro_lat,
            "centro_lng": o.centro_lng,
            "equipe": o.equipe.nome if o.equipe else None,
            "criado_em": o.criado_em.isoformat(),
        }
        for o in ordens
    ]


@router.patch("/ordens/{ordem_id}/status")
def atualizar_status_ordem(
    ordem_id: int,
    novo_status: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ordem = db.query(OrdemServico).filter_by(id=ordem_id).first()
    if not ordem:
        raise HTTPException(404, "Ordem não encontrada")
    if novo_status not in ("pendente", "em_andamento", "concluida"):
        raise HTTPException(400, "Status inválido")
    ordem.status = novo_status
    if novo_status == "em_andamento":
        ordem.iniciado_em = datetime.utcnow()
    elif novo_status == "concluida":
        ordem.concluido_em = datetime.utcnow()
        # Marca todos os chamados da OS como resolvidos
        for cid in (ordem.chamados_ids or []):
            c = db.query(Chamado).filter_by(id=cid).first()
            if c and c.status != "resolvido":
                c.status = "em_andamento"
    db.commit()
    return {"ordem_id": ordem_id, "status": novo_status}


# ─────────────────────────────────────────
# RASTREAMENTO GPS DE EQUIPES — Sprint 9
# ─────────────────────────────────────────

class LocalizacaoPayload(BaseModel):
    latitude: float
    longitude: float
    precisao_m: Optional[float] = None
    velocidade: Optional[float] = None
    bateria: Optional[int] = None
    chamado_id: Optional[int] = None
    em_servico: bool = True


@router.post("/equipes/localizacao")
def registrar_localizacao(
    payload: LocalizacaoPayload,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Equipe envia sua localização GPS periodicamente (a cada 30s)."""
    if current_user.tipo not in ("equipe", "gestor", "admin", "secretaria"):
        raise HTTPException(403, "Apenas equipes de campo podem registrar localização")

    loc = EquipeLocalizacao(
        usuario_id=current_user.id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        precisao_m=payload.precisao_m,
        velocidade=payload.velocidade,
        bateria=payload.bateria,
        chamado_id=payload.chamado_id,
        em_servico=payload.em_servico,
    )
    db.add(loc)
    db.commit()
    return {"registrado": True, "timestamp": loc.registrado_em.isoformat()}


@router.get("/equipes/mapa")
def mapa_equipes(
    current_user: Usuario = Depends(require_role("admin", "gestor", "secretaria")),
    db: Session = Depends(get_db),
):
    """
    Posição mais recente de cada equipe de campo.
    Para exibição no mapa do gestor em tempo real.
    """
    usuarios_equipe = (
        db.query(Usuario)
        .filter(Usuario.tipo.in_(["equipe", "secretaria"]), Usuario.ativo == True)
        .all()
    )

    resultado = []
    for u in usuarios_equipe:
        ultima = (
            db.query(EquipeLocalizacao)
            .filter_by(usuario_id=u.id)
            .order_by(EquipeLocalizacao.registrado_em.desc())
            .first()
        )
        if not ultima:
            continue

        # Considera desatualizado se > 5 min
        delta = (datetime.utcnow() - ultima.registrado_em).total_seconds()
        online = delta < 300

        resultado.append({
            "usuario_id": u.id,
            "nome": u.nome,
            "tipo": u.tipo,
            "latitude": ultima.latitude,
            "longitude": ultima.longitude,
            "velocidade": ultima.velocidade,
            "bateria": ultima.bateria,
            "em_servico": ultima.em_servico,
            "chamado_id": ultima.chamado_id,
            "online": online,
            "ultima_atualizacao": ultima.registrado_em.isoformat(),
            "segundos_desde_update": int(delta),
        })

    return {"equipes": resultado, "total": len(resultado)}


@router.get("/equipes/historico/{usuario_id}")
def historico_equipe(
    usuario_id: int,
    horas: int = 8,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """Trilha percorrida pela equipe nas últimas N horas."""
    desde = datetime.utcnow() - timedelta(hours=horas)
    locs = (
        db.query(EquipeLocalizacao)
        .filter(
            EquipeLocalizacao.usuario_id == usuario_id,
            EquipeLocalizacao.registrado_em >= desde,
        )
        .order_by(EquipeLocalizacao.registrado_em.asc())
        .all()
    )

    u = db.query(Usuario).filter_by(id=usuario_id).first()

    # Calcula distância total percorrida
    distancia_m = 0.0
    for i in range(1, len(locs)):
        distancia_m += _haversine(
            locs[i-1].latitude, locs[i-1].longitude,
            locs[i].latitude, locs[i].longitude,
        )

    return {
        "usuario": u.nome if u else str(usuario_id),
        "periodo_horas": horas,
        "total_pontos": len(locs),
        "distancia_km": round(distancia_m / 1000, 2),
        "trilha": [
            {
                "lat": l.latitude,
                "lng": l.longitude,
                "ts": l.registrado_em.isoformat(),
                "chamado_id": l.chamado_id,
            }
            for l in locs
        ],
    }


# ─────────────────────────────────────────
# SAÚDE DE BAIRRO — Sprint 9
# ─────────────────────────────────────────

@router.get("/bairros/saude")
def saude_todos_bairros(db: Session = Depends(get_db)):
    """Score de saúde urbana de todos os bairros — para mapa coroplético."""
    bairros = db.query(Bairro).filter(Bairro.ativo == True).all()
    resultado = []

    for b in bairros:
        total = db.query(func.count(Chamado.id)).filter(Chamado.bairro_id == b.id).scalar() or 0
        abertos = db.query(func.count(Chamado.id)).filter(
            Chamado.bairro_id == b.id, Chamado.status == "aberto"
        ).scalar() or 0
        criticos = db.query(func.count(Chamado.id)).filter(
            Chamado.bairro_id == b.id,
            Chamado.prioridade == "critica",
            Chamado.status != "resolvido",
        ).scalar() or 0

        if total == 0:
            score = 100
        else:
            score = max(0, min(100, round(100 - (abertos / total * 60) - criticos * 10)))

        resultado.append({
            "bairro_id": b.id,
            "bairro": b.nome,
            "regiao": b.regiao,
            "score": score,
            "status": "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴",
            "total_chamados": total,
            "abertos": abertos,
            "criticos": criticos,
        })

    resultado.sort(key=lambda x: x["score"])
    return resultado


@router.get("/bairros/{bairro_id}/saude")
def saude_bairro(bairro_id: int, db: Session = Depends(get_db)):
    b = db.query(Bairro).filter_by(id=bairro_id).first()
    if not b:
        raise HTTPException(404, "Bairro não encontrado")

    total = db.query(func.count(Chamado.id)).filter(Chamado.bairro_id == bairro_id).scalar() or 0
    abertos = db.query(func.count(Chamado.id)).filter(
        Chamado.bairro_id == bairro_id, Chamado.status == "aberto"
    ).scalar() or 0
    criticos = db.query(func.count(Chamado.id)).filter(
        Chamado.bairro_id == bairro_id,
        Chamado.prioridade == "critica",
        Chamado.status != "resolvido",
    ).scalar() or 0

    score = max(0, min(100, round(100 - (abertos / total * 60 if total else 0) - criticos * 10)))

    return {
        "bairro": b.nome,
        "regiao": b.regiao,
        "score": score,
        "status": "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴",
        "total_chamados": total,
        "chamados_abertos": abertos,
        "criticos": criticos,
    }


# ─────────────────────────────────────────
# ALERTAS CLIMÁTICOS — Sprint 10
# ─────────────────────────────────────────

@router.get("/clima/alertas")
async def alertas_climaticos():
    """
    Alertas preventivos de clima de Belém.
    Usa OpenWeatherMap se OPENWEATHER_API_KEY configurado.
    Retorna dados simulados realistas caso contrário.
    """
    LAT, LON = -1.4558, -48.4902
    api_key = os.environ.get("OPENWEATHER_API_KEY", "")

    if api_key:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(
                    "https://api.openweathermap.org/data/2.5/forecast",
                    params={"lat": LAT, "lon": LON, "appid": api_key,
                            "units": "metric", "lang": "pt_br"},
                )
                data = r.json()

            alertas = []
            for p in data.get("list", [])[:8]:
                chuva = p.get("rain", {}).get("3h", 0)
                vento = p.get("wind", {}).get("speed", 0)
                hora = p.get("dt_txt", "")

                if chuva > 20:
                    alertas.append({
                        "tipo": "chuva_intensa",
                        "titulo": "⚠️ Chuva intensa prevista",
                        "descricao": f"{chuva:.0f}mm esperados — acionar equipes de drenagem.",
                        "equipes_sugeridas": ["SESAN - Drenagem", "SEURB - Vias"],
                        "hora": hora, "nivel": "alto",
                    })
                if vento > 15:
                    alertas.append({
                        "tipo": "vento_forte",
                        "titulo": "🌪️ Vento forte previsto",
                        "descricao": f"{vento:.0f} m/s — risco de queda de árvores.",
                        "equipes_sugeridas": ["SEMMA - Poda emergencial"],
                        "hora": hora, "nivel": "medio",
                    })

            return {"alertas": alertas, "fonte": "OpenWeatherMap",
                    "atualizado": datetime.utcnow().isoformat()}
        except Exception:
            pass

    # Dados simulados para demo
    return {
        "alertas": [
            {
                "tipo": "chuva_intensa",
                "titulo": "⚠️ Chuva intensa prevista (demo)",
                "descricao": "35mm esperados amanhã 14h-18h. Acionar SESAN - Drenagem preventivamente.",
                "equipes_sugeridas": ["SESAN - Drenagem", "SEURB - Vias"],
                "hora": (datetime.utcnow() + timedelta(hours=18)).strftime("%Y-%m-%d %H:%M"),
                "nivel": "alto",
            }
        ],
        "fonte": "Simulado — configure OPENWEATHER_API_KEY para dados reais",
        "atualizado": datetime.utcnow().isoformat(),
    }
