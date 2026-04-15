"""
Sprint 19 — Inovações: Protocolo Público, Reincidência, Performance por Secretaria,
             Mapa Temporal, Notificação de Vizinhança, Widget, Sentimento, Full-Text
"""
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, text, and_
from pydantic import BaseModel

from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.historico import ChamadoHistorico
from app.models.usuario import Usuario
from app.models.bairro import Bairro
from app.models.categoria import Categoria
from app.utils.auth import get_current_user, require_role
from app.utils.rate_limit import check_rate_limit, get_client_ip

router = APIRouter(prefix="/api/inovacoes", tags=["Inovações Sprint 19"])


# ═══════════════════════════════════════════════════════════
# 1. CONSULTA PÚBLICA POR PROTOCOLO — sem login
# ═══════════════════════════════════════════════════════════

@router.get("/protocolo/{protocolo}")
def consulta_publica_protocolo(
    protocolo: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Cidadão consulta o status do chamado pelo número de protocolo sem precisar de login.
    Rate limit: 20 consultas/min por IP.
    Retorna dados anonimizados — sem nome ou contato do solicitante.
    """
    ip = get_client_ip(request)
    check_rate_limit(f"protocolo:{ip}", max_attempts=20, window_seconds=60)

    chamado = db.query(Chamado).filter(
        Chamado.protocolo == protocolo.upper()
    ).first()
    if not chamado:
        raise HTTPException(404, f"Protocolo {protocolo.upper()} não encontrado")

    historico = (
        db.query(ChamadoHistorico)
        .filter(ChamadoHistorico.chamado_id == chamado.id)
        .order_by(ChamadoHistorico.criado_em.asc())
        .all()
    )

    # Previsão simples de resolução baseada no SLA da categoria
    previsao_resolucao = None
    if chamado.status not in ("resolvido", "cancelado") and chamado.categoria:
        sla_h = chamado.categoria.sla_horas or 72
        previsao_resolucao = (chamado.created_at + timedelta(hours=sla_h)).isoformat()

    return {
        "protocolo": chamado.protocolo,
        "titulo": chamado.titulo,
        "descricao": chamado.descricao[:300] + "..." if len(chamado.descricao) > 300 else chamado.descricao,
        "status": chamado.status,
        "prioridade": chamado.prioridade,
        "categoria": chamado.categoria.nome if chamado.categoria else None,
        "bairro": chamado.bairro.nome if chamado.bairro else None,
        "endereco": chamado.endereco,
        "total_votos": chamado.total_votos or 0,
        "avaliacao": chamado.avaliacao,
        "criado_em": chamado.created_at.isoformat() if chamado.created_at else None,
        "resolvido_em": chamado.data_resolucao.isoformat() if chamado.data_resolucao else None,
        "previsao_resolucao": previsao_resolucao,
        "historico": [
            {
                "evento": h.campo,
                "de": h.valor_anterior,
                "para": h.valor_novo,
                "data": h.criado_em.isoformat() if h.criado_em else None,
                "observacao": h.observacao,
            }
            for h in historico
            if h.campo in ("status", "prioridade", "reclassificacao", "criacao")
        ],
        "link_compartilhavel": f"/consulta/{chamado.protocolo}",
    }


# ═══════════════════════════════════════════════════════════
# 2. DETECTOR DE REINCIDÊNCIA
# ═══════════════════════════════════════════════════════════

@router.get("/reincidencias")
def detectar_reincidencias(
    dias: int = 90,
    raio_metros: float = 50.0,
    min_ocorrencias: int = 2,
    current_user: Usuario = Depends(require_role("admin", "gestor", "secretaria")),
    db: Session = Depends(get_db),
):
    """
    Detecta problemas que voltaram a aparecer no mesmo local após resolução.
    Útil para priorizar obras definitivas vs. remendos paliativoss.
    """
    import math

    desde = datetime.now(timezone.utc) - timedelta(days=dias)

    # Pega chamados resolvidos com GPS no período
    resolvidos = db.query(Chamado).filter(
        Chamado.status == "resolvido",
        Chamado.latitude.isnot(None),
        Chamado.data_resolucao >= desde,
    ).all()

    # Pega chamados abertos com GPS (possíveis reincidências)
    abertos = db.query(Chamado).filter(
        Chamado.status.in_(["aberto", "em_andamento"]),
        Chamado.latitude.isnot(None),
    ).all()

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000
        p1, p2 = math.radians(lat1), math.radians(lat2)
        a = (math.sin(math.radians(lat2 - lat1) / 2) ** 2
             + math.cos(p1) * math.cos(p2)
             * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
        return 2 * R * math.asin(math.sqrt(a))

    reincidencias = []
    visitados = set()

    for r in resolvidos:
        if r.id in visitados:
            continue
        proximos_abertos = [
            a for a in abertos
            if haversine(r.latitude, r.longitude, a.latitude, a.longitude) <= raio_metros
            and (r.categoria_id is None or a.categoria_id == r.categoria_id)
        ]
        proximos_resolvidos = [
            r2 for r2 in resolvidos
            if r2.id != r.id and r2.id not in visitados
            and haversine(r.latitude, r.longitude, r2.latitude, r2.longitude) <= raio_metros
            and (r.categoria_id is None or r2.categoria_id == r.categoria_id)
        ]

        total = 1 + len(proximos_resolvidos) + len(proximos_abertos)
        if total >= min_ocorrencias:
            for r2 in proximos_resolvidos:
                visitados.add(r2.id)
            visitados.add(r.id)

            reincidencias.append({
                "local": r.endereco or f"{r.latitude:.4f},{r.longitude:.4f}",
                "bairro": r.bairro.nome if r.bairro else None,
                "categoria": r.categoria.nome if r.categoria else None,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "total_ocorrencias": total,
                "resolvidos_anteriores": len(proximos_resolvidos) + 1,
                "abertos_atuais": len(proximos_abertos),
                "alerta": "Reincidência — considerar obra definitiva",
                "chamados_ids": (
                    [r.id] + [r2.id for r2 in proximos_resolvidos]
                    + [a.id for a in proximos_abertos]
                ),
            })

    reincidencias.sort(key=lambda x: x["total_ocorrencias"], reverse=True)
    return {
        "periodo_dias": dias,
        "raio_metros": raio_metros,
        "total_pontos_reincidentes": len(reincidencias),
        "reincidencias": reincidencias[:50],  # top 50
    }


# ═══════════════════════════════════════════════════════════
# 3. PERFORMANCE POR SECRETARIA
# ═══════════════════════════════════════════════════════════

@router.get("/secretarias/performance")
def performance_secretarias(
    dias: int = 30,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """
    Ranking de desempenho das secretarias: tempo médio de resolução,
    taxa de SLA cumprido e tendência. Base para relatório COP 30.
    """
    from app.models.secretaria import Secretaria

    desde = datetime.now(timezone.utc) - timedelta(days=dias)
    secretarias = db.query(Secretaria).filter(Secretaria.ativa == True).all()

    resultado = []
    for sec in secretarias:
        chamados = db.query(Chamado).filter(
            Chamado.secretaria_id == sec.id,
            Chamado.created_at >= desde,
        ).all()

        if not chamados:
            continue

        total = len(chamados)
        resolvidos = [c for c in chamados if c.status == "resolvido" and c.data_resolucao]
        n_resolvidos = len(resolvidos)

        # Tempo médio de resolução em horas
        tempos = [
            (c.data_resolucao - c.created_at).total_seconds() / 3600
            for c in resolvidos
        ]
        tempo_medio_h = round(sum(tempos) / len(tempos), 1) if tempos else None

        # Taxa SLA: resolvidos dentro do SLA da categoria
        dentro_sla = sum(
            1 for c in resolvidos
            if c.categoria and c.categoria.sla_horas
            and (c.data_resolucao - c.created_at).total_seconds() / 3600 <= c.categoria.sla_horas
        )
        taxa_sla = round(dentro_sla / n_resolvidos * 100, 1) if n_resolvidos else 0

        # Avaliação média
        avaliacoes = [c.avaliacao for c in chamados if c.avaliacao is not None]
        avaliacao_media = round(sum(avaliacoes) / len(avaliacoes), 1) if avaliacoes else None

        resultado.append({
            "secretaria_id": sec.id,
            "secretaria": sec.nome,
            "sigla": sec.sigla if hasattr(sec, "sigla") else sec.nome[:6],
            "total_chamados": total,
            "resolvidos": n_resolvidos,
            "taxa_resolucao": round(n_resolvidos / total * 100, 1),
            "tempo_medio_resolucao_h": tempo_medio_h,
            "taxa_sla_cumprido": taxa_sla,
            "avaliacao_media": avaliacao_media,
            "score": round((taxa_sla * 0.5) + (min(avaliacao_media or 0, 5) / 5 * 30) + (taxa_sla * 0.2), 1),
            "alerta_baixo_desempenho": taxa_sla < 60 or (tempo_medio_h and tempo_medio_h > 120),
        })

    resultado.sort(key=lambda x: x["score"], reverse=True)
    return {
        "periodo_dias": dias,
        "secretarias": resultado,
        "melhor": resultado[0]["secretaria"] if resultado else None,
        "pior": resultado[-1]["secretaria"] if resultado else None,
        "gerado_em": datetime.now(timezone.utc).isoformat(),
    }


# ═══════════════════════════════════════════════════════════
# 4. MAPA DE CALOR TEMPORAL (dia × hora)
# ═══════════════════════════════════════════════════════════

@router.get("/heatmap-temporal")
def heatmap_temporal(
    dias: int = 90,
    categoria_id: Optional[int] = None,
    bairro_id: Optional[int] = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Matriz 7×24 (dias da semana × horas do dia) com volume de chamados.
    Permite descobrir padrões: "iluminação é mais reportada sextas às 19h".
    """
    DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    desde = datetime.now(timezone.utc) - timedelta(days=dias)
    query = db.query(Chamado).filter(Chamado.created_at >= desde)

    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)
    if bairro_id:
        query = query.filter(Chamado.bairro_id == bairro_id)

    chamados = query.all()

    # Inicializa matriz 7x24
    matriz = [[0] * 24 for _ in range(7)]
    for c in chamados:
        if c.created_at:
            dow = c.created_at.weekday()   # 0=segunda … 6=domingo
            hora = c.created_at.hour
            matriz[dow][hora] += 1

    # Encontra pico
    pico_val = max(max(row) for row in matriz)
    pico_info = None
    for d, row in enumerate(matriz):
        for h, val in enumerate(row):
            if val == pico_val:
                pico_info = {"dia": DIAS_SEMANA[d], "hora": f"{h:02d}h", "chamados": val}

    return {
        "periodo_dias": dias,
        "total_chamados": len(chamados),
        "matriz": [
            {
                "dia": DIAS_SEMANA[i],
                "horas": [{"hora": f"{h:02d}h", "total": matriz[i][h]} for h in range(24)],
                "total_dia": sum(matriz[i]),
            }
            for i in range(7)
        ],
        "pico": pico_info,
        "insight": (
            f"Pico de chamados: {pico_info['dia']} às {pico_info['hora']} "
            f"({pico_info['chamados']} chamados)"
        ) if pico_info else None,
    }


# ═══════════════════════════════════════════════════════════
# 5. NOTIFICAÇÃO DE VIZINHANÇA
# ═══════════════════════════════════════════════════════════

@router.post("/notificar-vizinhanca/{chamado_id}")
def notificar_vizinhanca(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Envia push notification para cidadãos do mesmo bairro sobre um chamado novo.
    Incentiva votos e mobilização. Apenas chamados com prioridade alta/critica.
    """
    from app.models.push_subscription import PushSubscription
    from app.routers.notificacoes_router import _enviar_webpush, PushPayload

    chamado = db.query(Chamado).filter_by(id=chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")

    if chamado.prioridade not in ("alta", "critica"):
        raise HTTPException(400, "Notificação de vizinhança apenas para chamados alta/crítica")

    if not chamado.bairro_id:
        raise HTTPException(400, "Chamado sem bairro definido")

    # Busca usuários do mesmo bairro com subscription ativa
    # Filtra os do próprio bairro via chamados (indiretamente)
    usuario_ids_bairro = (
        db.query(Chamado.usuario_id)
        .filter(
            Chamado.bairro_id == chamado.bairro_id,
            Chamado.usuario_id != chamado.usuario_id,
        )
        .distinct()
        .limit(200)
        .all()
    )
    ids = [uid for (uid,) in usuario_ids_bairro]

    subs = db.query(PushSubscription).filter(
        PushSubscription.usuario_id.in_(ids),
        PushSubscription.ativa == True,
    ).all()

    payload = PushPayload(
        titulo=f"🚨 Novo problema em {chamado.bairro.nome}",
        corpo=f"{chamado.titulo} — Vote para priorizar!",
        url=f"/app?protocolo={chamado.protocolo}",
    )

    enviadas, falhas = 0, 0
    for sub in subs:
        try:
            _enviar_webpush(sub.endpoint, sub.keys, payload)
            enviadas += 1
        except Exception:
            falhas += 1

    return {
        "chamado_protocolo": chamado.protocolo,
        "bairro": chamado.bairro.nome,
        "cidadaos_notificados": enviadas,
        "falhas": falhas,
        "subscriptions_encontradas": len(subs),
    }


# ═══════════════════════════════════════════════════════════
# 6. WIDGET INCORPORÁVEL
# ═══════════════════════════════════════════════════════════

@router.get("/widget/{bairro_id}")
def widget_bairro(
    bairro_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Dados para widget incorporável em sites e blogs de bairro.
    Retorna JSON leve ou HTML pronto para embed via iframe.
    Rate limit: 60 req/min por IP.
    """
    ip = get_client_ip(request)
    check_rate_limit(f"widget:{ip}", max_attempts=60, window_seconds=60)

    bairro = db.query(Bairro).filter_by(id=bairro_id).first()
    if not bairro:
        raise HTTPException(404, "Bairro não encontrado")

    total = db.query(func.count(Chamado.id)).filter(Chamado.bairro_id == bairro_id).scalar() or 0
    abertos = db.query(func.count(Chamado.id)).filter(
        Chamado.bairro_id == bairro_id, Chamado.status == "aberto"
    ).scalar() or 0
    resolvidos_30d = db.query(func.count(Chamado.id)).filter(
        Chamado.bairro_id == bairro_id,
        Chamado.status == "resolvido",
        Chamado.data_resolucao >= datetime.now(timezone.utc) - timedelta(days=30),
    ).scalar() or 0

    score = max(0, min(100, round(100 - (abertos / total * 60 if total else 0))))
    status_icon = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"

    ultimos = (
        db.query(Chamado)
        .filter(Chamado.bairro_id == bairro_id)
        .order_by(Chamado.created_at.desc())
        .limit(3)
        .all()
    )

    return {
        "bairro": bairro.nome,
        "score_saude": score,
        "status": status_icon,
        "abertos": abertos,
        "resolvidos_30d": resolvidos_30d,
        "total_historico": total,
        "ultimos_chamados": [
            {"protocolo": c.protocolo, "titulo": c.titulo[:60], "status": c.status}
            for c in ultimos
        ],
        "atualizado": datetime.now(timezone.utc).isoformat(),
        "embed_url": f"/api/inovacoes/widget/{bairro_id}",
        "embed_html": (
            f'<iframe src="https://zeladoria-backend-production.up.railway.app/api/inovacoes/widget/{bairro_id}" '
            f'width="320" height="200" frameborder="0" title="Zelô — {bairro.nome}"></iframe>'
        ),
    }


# ═══════════════════════════════════════════════════════════
# 7. ANÁLISE DE SENTIMENTO NAS AVALIAÇÕES
# ═══════════════════════════════════════════════════════════

_NEGATIVOS = ["demora", "demorou", "lento", "péssimo", "ruim", "horrível",
              "não resolveu", "voltou", "mesma coisa", "decepcionante", "insatisfeito",
              "descaso", "abandonado", "esqueceram", "ninguém", "sem retorno"]
_POSITIVOS = ["rápido", "ótimo", "excelente", "parabéns", "eficiente", "resolveu",
              "satisfeito", "perfeito", "muito bom", "agradeço", "obrigado"]


def _analisar_sentimento(texto: str) -> dict:
    t = texto.lower()
    neg = sum(1 for p in _NEGATIVOS if p in t)
    pos = sum(1 for p in _POSITIVOS if p in t)
    if neg > pos:
        return {"sentimento": "negativo", "score": -neg, "palavras_chave": [p for p in _NEGATIVOS if p in t]}
    if pos > neg:
        return {"sentimento": "positivo", "score": pos, "palavras_chave": [p for p in _POSITIVOS if p in t]}
    return {"sentimento": "neutro", "score": 0, "palavras_chave": []}


@router.get("/sentimento/avaliacoes")
def sentimento_avaliacoes(
    dias: int = 30,
    categoria_id: Optional[int] = None,
    secretaria_id: Optional[int] = None,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """
    Análise de sentimento dos comentários de avaliação por secretaria/categoria.
    Detecta padrões de insatisfação e palavras mais frequentes.
    """
    desde = datetime.now(timezone.utc) - timedelta(days=dias)
    query = db.query(Chamado).filter(
        Chamado.comentario_avaliacao.isnot(None),
        Chamado.created_at >= desde,
    )
    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)
    if secretaria_id:
        query = query.filter(Chamado.secretaria_id == secretaria_id)

    chamados = query.all()

    negativos, positivos, neutros = [], [], []
    palavras_negativas: dict = {}
    palavras_positivas: dict = {}

    for c in chamados:
        if not c.comentario_avaliacao:
            continue
        r = _analisar_sentimento(c.comentario_avaliacao)
        item = {
            "protocolo": c.protocolo,
            "avaliacao": c.avaliacao,
            "comentario": c.comentario_avaliacao[:120],
            "categoria": c.categoria.nome if c.categoria else None,
            "palavras": r["palavras_chave"],
        }
        if r["sentimento"] == "negativo":
            negativos.append(item)
            for p in r["palavras_chave"]:
                palavras_negativas[p] = palavras_negativas.get(p, 0) + 1
        elif r["sentimento"] == "positivo":
            positivos.append(item)
            for p in r["palavras_chave"]:
                palavras_positivas[p] = palavras_positivas.get(p, 0) + 1
        else:
            neutros.append(item)

    total = len(negativos) + len(positivos) + len(neutros)
    return {
        "periodo_dias": dias,
        "total_avaliacoes_com_texto": total,
        "resumo": {
            "negativos": len(negativos),
            "positivos": len(positivos),
            "neutros": len(neutros),
            "taxa_negatividade": round(len(negativos) / total * 100, 1) if total else 0,
        },
        "top_reclamacoes": sorted(palavras_negativas.items(), key=lambda x: -x[1])[:10],
        "top_elogios": sorted(palavras_positivas.items(), key=lambda x: -x[1])[:10],
        "avaliacoes_negativas": negativos[:20],
        "alerta": len(negativos) / total > 0.4 if total else False,
    }


# ═══════════════════════════════════════════════════════════
# 8. BUSCA FULL-TEXT
# ═══════════════════════════════════════════════════════════

@router.get("/busca")
def busca_fulltext(
    q: str,
    status: Optional[str] = None,
    bairro_id: Optional[int] = None,
    limite: int = 20,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Busca full-text em título, descrição e endereço dos chamados.
    PostgreSQL: usa ILIKE multi-token para busca relevante.
    SQLite: fallback com tokenização simples.
    Cidadão vê apenas seus próprios chamados.
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(400, "Busca deve ter pelo menos 2 caracteres")

    q = q.strip()[:200]
    tokens = [t.strip() for t in q.split() if len(t.strip()) >= 2][:8]

    query = db.query(Chamado)

    if current_user.tipo == "cidadao":
        query = query.filter(Chamado.usuario_id == current_user.id)
    if status:
        query = query.filter(Chamado.status == status)
    if bairro_id:
        query = query.filter(Chamado.bairro_id == bairro_id)

    # Filtro: qualquer token encontrado em título, descrição ou endereço
    from sqlalchemy import or_
    condicoes = []
    for tok in tokens:
        like = f"%{tok}%"
        condicoes.append(
            or_(
                Chamado.titulo.ilike(like),
                Chamado.descricao.ilike(like),
                Chamado.endereco.ilike(like),
                Chamado.protocolo.ilike(like),
            )
        )

    if condicoes:
        from sqlalchemy import and_
        query = query.filter(and_(*condicoes))

    total = query.count()
    chamados = query.order_by(Chamado.created_at.desc()).limit(min(limite, 100)).all()

    return {
        "query": q,
        "tokens": tokens,
        "total": total,
        "resultados": [
            {
                "id": c.id,
                "protocolo": c.protocolo,
                "titulo": c.titulo,
                "status": c.status,
                "prioridade": c.prioridade,
                "bairro": c.bairro.nome if c.bairro else None,
                "categoria": c.categoria.nome if c.categoria else None,
                "criado_em": c.created_at.isoformat() if c.created_at else None,
            }
            for c in chamados
        ],
    }
