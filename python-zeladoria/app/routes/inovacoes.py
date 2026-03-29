"""
Novas funcionalidades inovadoras do Zelô
- Votação em chamados
- Gamificação (pontos)
- Relatório público
- Agrupamento geoespacial
- Mapa de calor
- Triagem por IA
- Alertas climáticos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.utils.auth import get_current_user
import math, os, httpx

router = APIRouter(prefix="/api/inovacoes", tags=["Inovações"])

# ─── VOTAÇÃO ────────────────────────────────────────────────────────────────

class VotoResponse(BaseModel):
    votos: int
    ja_votou: bool

@router.post("/chamados/{chamado_id}/votar")
def votar_chamado(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")

    # Usa campo de comentario_avaliacao para guardar votos (evita nova migração)
    # Formato: "VOTOS:N:user1,user2,..."
    votos_raw = chamado.comentario_avaliacao or ""
    
    if votos_raw.startswith("VOTOS:"):
        parts = votos_raw.split(":")
        count = int(parts[1]) if len(parts) > 1 else 0
        voters = parts[2].split(",") if len(parts) > 2 and parts[2] else []
    else:
        count = 0
        voters = []

    user_str = str(current_user.id)
    
    if user_str in voters:
        # Remover voto
        voters.remove(user_str)
        count = max(0, count - 1)
        ja_votou = False
    else:
        # Adicionar voto
        voters.append(user_str)
        count += 1
        ja_votou = True
        # Aumentar prioridade automaticamente com muitos votos
        if count >= 10 and chamado.prioridade == "media":
            chamado.prioridade = "alta"
        elif count >= 25 and chamado.prioridade == "alta":
            chamado.prioridade = "critica"

    chamado.comentario_avaliacao = f"VOTOS:{count}:{','.join(voters)}"
    db.commit()
    
    # Gamificação: quem reportou o chamado ganha pontos
    _adicionar_pontos(db, chamado.usuario_id, 2, "voto_recebido")
    
    return {"votos": count, "ja_votou": ja_votou}

@router.get("/chamados/{chamado_id}/votos")
def ver_votos(chamado_id: int, db: Session = Depends(get_db)):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    votos_raw = chamado.comentario_avaliacao or ""
    if votos_raw.startswith("VOTOS:"):
        parts = votos_raw.split(":")
        count = int(parts[1]) if len(parts) > 1 else 0
    else:
        count = 0
    return {"votos": count}

# ─── GAMIFICAÇÃO ─────────────────────────────────────────────────────────────

def _adicionar_pontos(db: Session, usuario_id: int, pontos: int, motivo: str):
    """Adiciona pontos de gamificação ao usuário (usa campo avatar para guardar pontos)"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return
    # Formato avatar: "PONTOS:N" (reutilizando campo para evitar migração)
    avatar_raw = usuario.avatar or ""
    if avatar_raw.startswith("PONTOS:"):
        atual = int(avatar_raw.split(":")[1])
    else:
        atual = 0
    usuario.avatar = f"PONTOS:{atual + pontos}"
    db.commit()

@router.get("/ranking")
def ranking_cidadaos(db: Session = Depends(get_db)):
    """Top cidadãos por pontos"""
    usuarios = db.query(Usuario).filter(
        Usuario.tipo == "cidadao",
        Usuario.avatar.like("PONTOS:%")
    ).all()
    
    ranking = []
    for u in usuarios:
        pontos = int(u.avatar.split(":")[1]) if u.avatar and u.avatar.startswith("PONTOS:") else 0
        chamados_count = db.query(func.count(Chamado.id)).filter(Chamado.usuario_id == u.id).scalar()
        ranking.append({
            "id": u.id,
            "nome": u.nome,
            "pontos": pontos,
            "chamados": chamados_count,
            "nivel": _calcular_nivel(pontos)
        })
    
    ranking.sort(key=lambda x: x["pontos"], reverse=True)
    return ranking[:20]

@router.get("/meu-perfil")
def meu_perfil_gamificacao(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    avatar_raw = current_user.avatar or ""
    pontos = int(avatar_raw.split(":")[1]) if avatar_raw.startswith("PONTOS:") else 0
    chamados_count = db.query(func.count(Chamado.id)).filter(Chamado.usuario_id == current_user.id).scalar()
    resolvidos = db.query(func.count(Chamado.id)).filter(
        Chamado.usuario_id == current_user.id,
        Chamado.status == "resolvido"
    ).scalar()
    
    return {
        "pontos": pontos,
        "nivel": _calcular_nivel(pontos),
        "proxima_conquista": _proxima_conquista(pontos),
        "chamados_abertos": chamados_count,
        "chamados_resolvidos": resolvidos,
        "conquistas": _listar_conquistas(pontos, chamados_count)
    }

def _calcular_nivel(pontos: int) -> dict:
    niveis = [
        (0, "Iniciante", "🌱"),
        (50, "Observador", "👁️"),
        (150, "Cidadão Ativo", "⚡"),
        (400, "Guardião", "🛡️"),
        (800, "Herói Urbano", "🦸"),
        (1500, "Lenda de Belém", "🏆"),
    ]
    nivel_atual = niveis[0]
    proximo = niveis[1] if len(niveis) > 1 else None
    for i, n in enumerate(niveis):
        if pontos >= n[0]:
            nivel_atual = n
            proximo = niveis[i+1] if i+1 < len(niveis) else None
    return {
        "nome": nivel_atual[2] + " " + nivel_atual[1],
        "min_pontos": nivel_atual[0],
        "proximo": proximo[1] if proximo else None,
        "proximo_min": proximo[0] if proximo else None
    }

def _proxima_conquista(pontos: int) -> str:
    if pontos < 50: return f"Faltam {50 - pontos} pontos para Observador"
    if pontos < 150: return f"Faltam {150 - pontos} pontos para Cidadão Ativo"
    if pontos < 400: return f"Faltam {400 - pontos} pontos para Guardião"
    if pontos < 800: return f"Faltam {800 - pontos} pontos para Herói Urbano"
    if pontos < 1500: return f"Faltam {1500 - pontos} pontos para Lenda de Belém"
    return "Você atingiu o nível máximo! 🏆"

def _listar_conquistas(pontos: int, chamados: int) -> list:
    conquistas = []
    if chamados >= 1: conquistas.append({"titulo": "Primeiro Passo", "desc": "Abriu seu primeiro chamado", "icone": "🎯", "desbloqueado": True})
    if chamados >= 5: conquistas.append({"titulo": "Vigilante", "desc": "5 chamados abertos", "icone": "👮", "desbloqueado": True})
    if chamados >= 10: conquistas.append({"titulo": "Fiscal Cidadão", "desc": "10 chamados abertos", "icone": "🔍", "desbloqueado": chamados >= 10})
    if pontos >= 100: conquistas.append({"titulo": "Centenário", "desc": "100 pontos conquistados", "icone": "💯", "desbloqueado": pontos >= 100})
    if pontos >= 500: conquistas.append({"titulo": "Meio Milhar", "desc": "500 pontos conquistados", "icone": "⭐", "desbloqueado": pontos >= 500})
    return conquistas

# ─── MAPA DE CALOR ───────────────────────────────────────────────────────────

@router.get("/mapa-calor")
def mapa_calor(
    status: Optional[str] = None,
    dias: int = 30,
    db: Session = Depends(get_db)
):
    """Retorna pontos para o heatmap"""
    desde = datetime.utcnow() - timedelta(days=dias)
    query = db.query(
        Chamado.latitude,
        Chamado.longitude,
        Chamado.prioridade,
        Chamado.status,
        Chamado.titulo
    ).filter(
        Chamado.latitude != None,
        Chamado.longitude != None,
        Chamado.created_at >= desde
    )
    
    if status:
        query = query.filter(Chamado.status == status)
    
    pontos = []
    peso_map = {"critica": 1.0, "alta": 0.7, "media": 0.4, "baixa": 0.2}
    
    for row in query.all():
        pontos.append({
            "lat": row.latitude,
            "lng": row.longitude,
            "peso": peso_map.get(row.prioridade, 0.4),
            "status": row.status,
            "titulo": row.titulo
        })
    
    return {"pontos": pontos, "total": len(pontos)}

# ─── AGRUPAMENTO GEOESPACIAL ─────────────────────────────────────────────────

@router.get("/clusters")
def agrupar_chamados(
    raio_metros: float = 100.0,
    db: Session = Depends(get_db)
):
    """Agrupa chamados abertos próximos geograficamente"""
    chamados = db.query(Chamado).filter(
        Chamado.status.in_(["aberto", "em_andamento"]),
        Chamado.latitude != None,
        Chamado.longitude != None
    ).all()
    
    clusters = []
    visitados = set()
    
    for i, c1 in enumerate(chamados):
        if i in visitados:
            continue
        cluster = [c1]
        visitados.add(i)
        for j, c2 in enumerate(chamados):
            if j in visitados:
                continue
            dist = _haversine(c1.latitude, c1.longitude, c2.latitude, c2.longitude)
            if dist <= raio_metros:
                cluster.append(c2)
                visitados.add(j)
        
        if len(cluster) > 1:
            lat_c = sum(c.latitude for c in cluster) / len(cluster)
            lng_c = sum(c.longitude for c in cluster) / len(cluster)
            clusters.append({
                "centro_lat": lat_c,
                "centro_lng": lng_c,
                "total": len(cluster),
                "chamados": [{"id": c.id, "protocolo": c.protocolo, "titulo": c.titulo} for c in cluster],
                "economia_estimada": f"{(len(cluster)-1) * 45} min de deslocamento economizados"
            })
    
    clusters.sort(key=lambda x: x["total"], reverse=True)
    return {"clusters": clusters, "total_agrupados": sum(c["total"] for c in clusters)}

def _haversine(lat1, lon1, lat2, lon2) -> float:
    """Distância em metros entre dois pontos GPS"""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return 2 * R * math.asin(math.sqrt(a))

# ─── TRIAGEM POR IA ───────────────────────────────────────────────────────────

@router.post("/triar")
def triar_chamado_ia(
    payload: dict,
    db: Session = Depends(get_db)
):
    """Sugere categoria, prioridade e secretaria baseado no texto"""
    descricao = payload.get("descricao", "").lower()
    titulo = payload.get("titulo", "").lower()
    texto = titulo + " " + descricao
    
    # Mapeamento inteligente por palavras-chave
    regras = [
        (["buraco", "cratera", "asfalto", "pavimento", "vala"], "Buraco na via", "alta", "SEURB"),
        (["luz", "lâmpada", "poste", "iluminação", "escuro"], "Iluminação pública", "alta", "SEURB"),
        (["calçada", "passeio", "piso", "pedestre"], "Calçada danificada", "media", "SEURB"),
        (["lixo", "entulho", "sujeira", "resíduo", "descarte"], "Lixo acumulado", "media", "SESAN"),
        (["esgoto", "valeta", "alagamento", "água parada", "bueiro"], "Esgoto", "alta", "SESAN"),
        (["árvore", "galho", "poda", "raiz", "vegeta"], "Poda de árvore", "media", "SEMMA"),
        (["dengue", "mosquito", "foco", "aedes", "larvicida"], "Foco de dengue", "critica", "SESMA"),
        (["placa", "semáforo", "sinalização", "faixa", "trânsito"], "Sinalização", "alta", "SEURB"),
        (["praça", "parque", "jardim", "área verde", "mato"], "Área verde", "baixa", "SEMMA"),
        (["segurança", "vandalismo", "crime", "violência", "furto"], "Segurança pública", "critica", "GMB"),
    ]
    
    melhor = None
    melhor_score = 0
    
    for palavras, categoria, prioridade, secretaria in regras:
        score = sum(1 for p in palavras if p in texto)
        if score > melhor_score:
            melhor_score = score
            melhor = (categoria, prioridade, secretaria)
    
    if not melhor:
        melhor = ("Outros", "media", "OGM")
    
    # Buscar categoria no banco
    cat = db.query(Categoria).filter(Categoria.nome.like(f"%{melhor[0].split()[0]}%")).first()
    
    return {
        "categoria_sugerida": melhor[0],
        "categoria_id": cat.id if cat else None,
        "prioridade_sugerida": melhor[1],
        "secretaria_sugerida": melhor[2],
        "confianca": min(melhor_score * 25, 95) if melhor_score > 0 else 40,
        "motivo": f"Detectei {melhor_score} palavras-chave relacionadas a '{melhor[0]}'"
    }

# ─── RELATÓRIO PÚBLICO ────────────────────────────────────────────────────────

@router.get("/relatorio-publico")
def relatorio_publico(
    mes: Optional[int] = None,
    ano: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Relatório público de prestação de contas"""
    if not mes:
        mes = datetime.utcnow().month
    if not ano:
        ano = datetime.utcnow().year
    
    inicio = datetime(ano, mes, 1)
    fim = datetime(ano, mes + 1, 1) if mes < 12 else datetime(ano + 1, 1, 1)
    
    total = db.query(func.count(Chamado.id)).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim
    ).scalar()
    
    resolvidos = db.query(func.count(Chamado.id)).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim,
        Chamado.status == "resolvido"
    ).scalar()
    
    abertos = db.query(func.count(Chamado.id)).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim,
        Chamado.status == "aberto"
    ).scalar()
    
    # Por categoria
    por_cat = db.query(
        Categoria.nome,
        func.count(Chamado.id).label("total")
    ).join(Chamado, Chamado.categoria_id == Categoria.id).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim
    ).group_by(Categoria.nome).order_by(text("total DESC")).limit(5).all()
    
    # Por bairro
    por_bairro = db.query(
        Bairro.nome,
        func.count(Chamado.id).label("total")
    ).join(Chamado, Chamado.bairro_id == Bairro.id).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim
    ).group_by(Bairro.nome).order_by(text("total DESC")).limit(5).all()
    
    taxa = round((resolvidos / total * 100) if total > 0 else 0, 1)
    
    return {
        "periodo": f"{mes:02d}/{ano}",
        "total_chamados": total,
        "resolvidos": resolvidos,
        "abertos": abertos,
        "taxa_resolucao": taxa,
        "top_categorias": [{"categoria": r[0], "total": r[1]} for r in por_cat],
        "top_bairros": [{"bairro": r[0], "total": r[1]} for r in por_bairro],
        "mensagem_prefeitura": f"Em {mes:02d}/{ano}, a Prefeitura de Belém atendeu {total} solicitações com taxa de resolução de {taxa}%.",
        "gerado_em": datetime.utcnow().isoformat()
    }

# ─── ALERTAS CLIMÁTICOS ───────────────────────────────────────────────────────

@router.get("/clima-alertas")
async def alertas_climaticos():
    """Alerta preventivo baseado no clima de Belém"""
    # Belém, PA coordenadas
    lat, lon = -1.4558, -48.4902
    
    try:
        api_key = os.environ.get("OPENWEATHER_API_KEY", "")
        if not api_key:
            # Dados simulados para demo
            return _clima_simulado()
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.openweathermap.org/data/2.5/forecast",
                params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "pt_br"},
                timeout=5.0
            )
            data = resp.json()
        
        alertas = []
        previsao_24h = data.get("list", [])[:8]  # próximas 24h (3h cada)
        
        for p in previsao_24h:
            chuva = p.get("rain", {}).get("3h", 0)
            vento = p.get("wind", {}).get("speed", 0)
            
            if chuva > 20:
                alertas.append({
                    "tipo": "chuva_intensa",
                    "titulo": "⚠️ Chuva intensa prevista",
                    "desc": f"{chuva:.0f}mm esperados. Acionar equipes de drenagem.",
                    "equipes": ["SESAN - Drenagem", "SEURB - Vias"],
                    "hora": p.get("dt_txt", "")
                })
            if vento > 15:
                alertas.append({
                    "tipo": "vento_forte",
                    "titulo": "🌪️ Vento forte previsto",
                    "desc": f"{vento:.0f} m/s. Risco de queda de árvores.",
                    "equipes": ["SEMMA - Poda emergencial"],
                    "hora": p.get("dt_txt", "")
                })
        
        return {"alertas": alertas, "fonte": "OpenWeatherMap", "atualizado": datetime.utcnow().isoformat()}
    
    except Exception:
        return _clima_simulado()

def _clima_simulado():
    """Dados de demonstração"""
    return {
        "alertas": [
            {
                "tipo": "chuva_intensa",
                "titulo": "⚠️ Chuva prevista para amanhã",
                "desc": "35mm esperados (14h-18h). Acionar equipes de drenagem preventivamente.",
                "equipes": ["SESAN - Drenagem", "SEURB - Vias"],
                "hora": (datetime.utcnow() + timedelta(hours=18)).strftime("%Y-%m-%d %H:%M")
            }
        ],
        "fonte": "Demonstração (configure OPENWEATHER_API_KEY para dados reais)",
        "atualizado": datetime.utcnow().isoformat()
    }

# ─── ESTATÍSTICAS DE BAIRRO ───────────────────────────────────────────────────

@router.get("/bairro/{bairro_id}/saude")
def saude_bairro(bairro_id: int, db: Session = Depends(get_db)):
    """Score de saúde urbana de um bairro"""
    total = db.query(func.count(Chamado.id)).filter(Chamado.bairro_id == bairro_id).scalar()
    abertos = db.query(func.count(Chamado.id)).filter(
        Chamado.bairro_id == bairro_id, Chamado.status == "aberto"
    ).scalar()
    criticos = db.query(func.count(Chamado.id)).filter(
        Chamado.bairro_id == bairro_id,
        Chamado.prioridade == "critica",
        Chamado.status != "resolvido"
    ).scalar()
    
    # Score de 0-100
    if total == 0:
        score = 100
    else:
        taxa_abertos = abertos / total
        penalidade_criticos = criticos * 10
        score = max(0, min(100, round(100 - (taxa_abertos * 60) - penalidade_criticos)))
    
    emoji = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"
    
    bairro = db.query(Bairro).filter(Bairro.id == bairro_id).first()
    return {
        "bairro": bairro.nome if bairro else "—",
        "score": score,
        "status": emoji,
        "total_chamados": total,
        "chamados_abertos": abertos,
        "criticos": criticos
    }
