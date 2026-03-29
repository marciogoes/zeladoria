"""
Sprints 11–12 — Inteligência Artificial
Triagem automática, análise de foto, previsão de demanda, relatório mensal
"""
import os, json
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.bairro import Bairro
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.sprints_9_12 import LogTriagemIA, PrevisaoDemanda, RelatorioMensal
from app.utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/ia", tags=["Inteligência Artificial"])


# ─────────────────────────────────────────
# Mapeamento regras de triagem
# ─────────────────────────────────────────
REGRAS_TRIAGEM = [
    (["buraco", "cratera", "asfalto", "pavimento", "vala", "buraco na pista"],
     "Buraco na via", "alta", "SEURB"),
    (["luz", "lâmpada", "poste", "iluminação", "escuro", "apagado", "sem luz"],
     "Iluminação pública", "alta", "SEURB"),
    (["calçada", "passeio", "piso", "pedestre", "calçamento"],
     "Calçada danificada", "media", "SEURB"),
    (["lixo", "entulho", "sujeira", "resíduo", "descarte", "lixão", "lixeira"],
     "Lixo acumulado", "media", "SESAN"),
    (["esgoto", "valeta", "alagamento", "água parada", "bueiro", "enchente", "inundação"],
     "Esgoto", "alta", "SESAN"),
    (["árvore", "galho", "poda", "raiz", "vegetação", "mato alto"],
     "Poda de árvore", "media", "SEMMA"),
    (["dengue", "mosquito", "foco", "aedes", "larvicida", "água empoçada"],
     "Foco de dengue", "critica", "SESMA"),
    (["placa", "semáforo", "sinalização", "faixa", "trânsito", "sinaleira"],
     "Sinalização", "alta", "SEURB"),
    (["praça", "parque", "jardim", "área verde", "mato", "capim"],
     "Área verde", "baixa", "SEMMA"),
    (["segurança", "vandalismo", "crime", "violência", "furto", "roubo"],
     "Segurança pública", "critica", "GMB"),
    (["animal", "cão", "gato", "abandonado", "ferido", "solto"],
     "Animal abandonado", "media", "SESMA"),
    (["obra", "construção", "canteiro", "bloqueio", "via bloqueada"],
     "Obra irregular", "media", "SEURB"),
]


def _aplicar_regras(texto: str) -> dict:
    """Triagem por palavras-chave — baseline sempre disponível."""
    t = texto.lower()
    melhor, melhor_score = None, 0
    for palavras, categoria, prioridade, secretaria in REGRAS_TRIAGEM:
        score = sum(1 for p in palavras if p in t)
        if score > melhor_score:
            melhor_score = score
            melhor = (categoria, prioridade, secretaria, score)

    if not melhor:
        return {"categoria": "Outros", "prioridade": "media",
                "secretaria": "OGM", "confianca": 0.35, "modelo": "regras"}

    confianca = min(melhor[3] * 0.20, 0.92)
    return {
        "categoria": melhor[0], "prioridade": melhor[1],
        "secretaria": melhor[2], "confianca": round(confianca, 2),
        "modelo": "regras",
    }


# ─────────────────────────────────────────
# TRIAGEM AUTOMÁTICA — Sprint 11
# ─────────────────────────────────────────

class TriagemPayload(BaseModel):
    titulo: str
    descricao: str
    chamado_id: Optional[int] = None


@router.post("/triar")
def triar_chamado(
    payload: TriagemPayload,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Classifica automaticamente um chamado por categoria, prioridade e secretaria.
    Usa regras por palavras-chave como baseline confiável.
    Registra o log para análise de acurácia.
    """
    texto = f"{payload.titulo} {payload.descricao}"
    resultado = _aplicar_regras(texto)

    # Busca categoria no banco pelo nome
    cat = db.query(Categoria).filter(
        Categoria.nome.ilike(f"%{resultado['categoria'].split()[0]}%")
    ).first()

    # Registra log
    log = LogTriagemIA(
        chamado_id=payload.chamado_id,
        texto_entrada=texto[:500],
        categoria_sugerida=resultado["categoria"],
        prioridade_sugerida=resultado["prioridade"],
        secretaria_sugerida=resultado["secretaria"],
        confianca=resultado["confianca"],
        modelo=resultado["modelo"],
    )
    db.add(log)
    db.commit()

    return {
        "categoria_sugerida": resultado["categoria"],
        "categoria_id": cat.id if cat else None,
        "prioridade_sugerida": resultado["prioridade"],
        "secretaria_sugerida": resultado["secretaria"],
        "confianca": resultado["confianca"],
        "modelo": resultado["modelo"],
        "log_id": log.id,
        "dica": "Revise as sugestões antes de confirmar. Confiança > 0.6 é recomendada para aceite automático.",
    }


@router.post("/triar/{log_id}/feedback")
def feedback_triagem(
    log_id: int,
    aceita: bool,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Gestor informa se aceitou a sugestão da IA — melhora métricas."""
    log = db.query(LogTriagemIA).filter_by(id=log_id).first()
    if not log:
        raise HTTPException(404, "Log de triagem não encontrado")
    log.aceita = aceita
    db.commit()
    return {"log_id": log_id, "aceita": aceita}


@router.get("/triagem/metricas")
def metricas_triagem(
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """Métricas de acurácia da triagem automática."""
    total = db.query(func.count(LogTriagemIA.id)).scalar() or 0
    com_feedback = db.query(func.count(LogTriagemIA.id)).filter(
        LogTriagemIA.aceita.isnot(None)
    ).scalar() or 0
    aceitas = db.query(func.count(LogTriagemIA.id)).filter(
        LogTriagemIA.aceita == True
    ).scalar() or 0
    conf_media = db.query(func.avg(LogTriagemIA.confianca)).scalar() or 0

    return {
        "total_triagens": total,
        "com_feedback": com_feedback,
        "aceitas": aceitas,
        "taxa_aceitacao": round(aceitas / com_feedback * 100, 1) if com_feedback else 0,
        "confianca_media": round(float(conf_media), 2),
    }


# ─────────────────────────────────────────
# ANÁLISE DE FOTO — Sprint 11
# ─────────────────────────────────────────

@router.post("/analisar-foto")
async def analisar_foto(
    foto: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Analisa uma foto e sugere categoria do problema.
    Detecta indicadores visuais por metadados do arquivo.
    Em produção: substituir pela API de visão do modelo.
    """
    if not foto.content_type or not foto.content_type.startswith("image/"):
        raise HTTPException(400, "Apenas imagens são aceitas (jpg, png, webp)")

    conteudo = await foto.read()
    tamanho_kb = len(conteudo) / 1024

    # Heurísticas por tamanho e nome do arquivo (baseline sem GPU)
    nome = (foto.filename or "").lower()
    sugestao = "Outros"
    confianca = 0.30

    indicadores = {
        "buraco": ["buraco", "asfalto", "pavimento", "vala", "cratera"],
        "lixo": ["lixo", "entulho", "sujeira", "lixeira"],
        "arvore": ["arvore", "galho", "poda", "planta"],
        "esgoto": ["esgoto", "agua", "vala", "valeta"],
        "iluminacao": ["luz", "poste", "lamp", "ilumina"],
    }

    CAT_MAP = {
        "buraco": ("Buraco na via", "alta"),
        "lixo": ("Lixo acumulado", "media"),
        "arvore": ("Poda de árvore", "media"),
        "esgoto": ("Esgoto", "alta"),
        "iluminacao": ("Iluminação pública", "alta"),
    }

    for chave, palavras in indicadores.items():
        if any(p in nome for p in palavras):
            sugestao, prioridade = CAT_MAP[chave]
            confianca = 0.55
            break
    else:
        prioridade = "media"

    return {
        "arquivo": foto.filename,
        "tamanho_kb": round(tamanho_kb, 1),
        "tipo": foto.content_type,
        "categoria_sugerida": sugestao,
        "prioridade_sugerida": prioridade,
        "confianca": confianca,
        "nota": "Análise baseada no nome do arquivo. Em produção, use API de visão computacional.",
    }


# ─────────────────────────────────────────
# PREVISÃO DE DEMANDA — Sprint 12
# ─────────────────────────────────────────

@router.get("/previsao/demanda")
def prever_demanda(
    semanas_futuro: int = 1,
    bairro_id: Optional[int] = None,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """
    Prevê volume de chamados das próximas semanas por bairro.
    Modelo: Média Móvel de 4 semanas (MA4) — confiável para séries sazonais.
    """
    agora = datetime.utcnow()
    previsoes = []

    bairros = db.query(Bairro).filter(Bairro.ativo == True)
    if bairro_id:
        bairros = bairros.filter(Bairro.id == bairro_id)

    for bairro in bairros.all():
        historico = []
        for w in range(4, 0, -1):
            inicio = agora - timedelta(weeks=w)
            fim = agora - timedelta(weeks=w - 1)
            n = db.query(func.count(Chamado.id)).filter(
                Chamado.bairro_id == bairro.id,
                Chamado.created_at >= inicio,
                Chamado.created_at < fim,
            ).scalar() or 0
            historico.append(n)

        ma4 = round(sum(historico) / len(historico)) if historico else 0

        for f in range(1, semanas_futuro + 1):
            ini_prev = agora + timedelta(weeks=f - 1)
            fim_prev = agora + timedelta(weeks=f)
            previsoes.append({
                "bairro_id": bairro.id,
                "bairro": bairro.nome,
                "regiao": bairro.regiao,
                "semana_inicio": ini_prev.strftime("%Y-%m-%d"),
                "semana_fim": fim_prev.strftime("%Y-%m-%d"),
                "previsao": ma4,
                "historico_4sem": historico,
                "modelo": "MA4",
                "alerta": ma4 > 10,
            })

    previsoes.sort(key=lambda x: x["previsao"], reverse=True)
    return {
        "previsoes": previsoes,
        "semanas_futuro": semanas_futuro,
        "gerado_em": agora.isoformat(),
        "modelo": "Média Móvel 4 semanas",
    }


@router.get("/previsao/categorias")
def prever_por_categoria(
    semanas: int = 4,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """Previsão de demanda por categoria — útil para alocar equipes."""
    agora = datetime.utcnow()
    resultado = []

    for cat in db.query(Categoria).all():
        historico = []
        for w in range(semanas, 0, -1):
            inicio = agora - timedelta(weeks=w)
            fim = agora - timedelta(weeks=w - 1)
            n = db.query(func.count(Chamado.id)).filter(
                Chamado.categoria_id == cat.id,
                Chamado.created_at >= inicio,
                Chamado.created_at < fim,
            ).scalar() or 0
            historico.append(n)

        ma = round(sum(historico) / len(historico)) if historico else 0
        tendencia = "alta" if historico and historico[-1] > historico[0] else "estável"

        resultado.append({
            "categoria_id": cat.id,
            "categoria": cat.nome,
            "icone": cat.icone,
            "cor": cat.cor,
            "previsao_semana": ma,
            "historico": historico,
            "tendencia": tendencia,
        })

    resultado.sort(key=lambda x: x["previsao_semana"], reverse=True)
    return resultado


# ─────────────────────────────────────────
# RELATÓRIO MENSAL — Sprint 12
# ─────────────────────────────────────────

@router.post("/relatorio/gerar")
def gerar_relatorio_mensal(
    mes: Optional[int] = None,
    ano: Optional[int] = None,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    """Gera snapshot completo do mês como relatório estruturado."""
    agora = datetime.utcnow()
    mes = mes or agora.month
    ano = ano or agora.year

    inicio = datetime(ano, mes, 1)
    fim = datetime(ano, mes + 1, 1) if mes < 12 else datetime(ano + 1, 1, 1)

    # Checa se já existe
    existente = db.query(RelatorioMensal).filter_by(ano=ano, mes=mes).first()

    total = db.query(func.count(Chamado.id)).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim
    ).scalar() or 0

    resolvidos = db.query(func.count(Chamado.id)).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim,
        Chamado.status == "resolvido",
    ).scalar() or 0

    abertos = db.query(func.count(Chamado.id)).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim,
        Chamado.status == "aberto",
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

    por_bairro = db.query(
        Bairro.nome, func.count(Chamado.id).label("total")
    ).join(Chamado, Chamado.bairro_id == Bairro.id).filter(
        Chamado.created_at >= inicio, Chamado.created_at < fim
    ).group_by(Bairro.nome).order_by(func.count(Chamado.id).desc()).limit(5).all()

    dados = {
        "periodo": f"{mes:02d}/{ano}",
        "total_chamados": total,
        "resolvidos": resolvidos,
        "abertos": abertos,
        "taxa_resolucao": round(resolvidos / total * 100, 1) if total else 0,
        "avaliacao_media": round(float(avaliacao), 1),
        "top_categorias": [{"categoria": c, "total": t} for c, t in por_cat],
        "top_bairros": [{"bairro": b, "total": t} for b, t in por_bairro],
        "gerado_em": agora.isoformat(),
        "gerado_por": current_user.nome,
    }

    if existente:
        existente.dados = dados
        existente.gerado_em = agora
        existente.gerado_por = current_user.nome
        db.commit()
        rel_id = existente.id
    else:
        rel = RelatorioMensal(ano=ano, mes=mes, dados=dados, gerado_por=current_user.nome)
        db.add(rel)
        db.commit()
        db.refresh(rel)
        rel_id = rel.id

    return {"relatorio_id": rel_id, **dados}


@router.get("/relatorio/{ano}/{mes}")
def obter_relatorio(
    ano: int,
    mes: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rel = db.query(RelatorioMensal).filter_by(ano=ano, mes=mes).first()
    if not rel:
        raise HTTPException(404, f"Relatório {mes:02d}/{ano} não encontrado. Gere primeiro via POST /api/ia/relatorio/gerar")
    return {"relatorio_id": rel.id, "ano": rel.ano, "mes": rel.mes, **rel.dados}


@router.get("/relatorio/historico")
def historico_relatorios(
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    rels = db.query(RelatorioMensal).order_by(
        RelatorioMensal.ano.desc(), RelatorioMensal.mes.desc()
    ).limit(24).all()

    return [
        {
            "id": r.id,
            "periodo": f"{r.mes:02d}/{r.ano}",
            "total_chamados": (r.dados or {}).get("total_chamados", 0),
            "taxa_resolucao": (r.dados or {}).get("taxa_resolucao", 0),
            "gerado_em": r.gerado_em.isoformat() if r.gerado_em else None,
        }
        for r in rels
    ]


# ─────────────────────────────────────────
# PAINEL PÚBLICO EM TEMPO REAL — Sprint 12
# (Para telão em locais públicos)
# ─────────────────────────────────────────

@router.get("/painel-publico")
def painel_publico_tempo_real(db: Session = Depends(get_db)):
    """
    Endpoint para painel em telão — sem autenticação, atualizado em tempo real.
    Mostra stats do dia, semana e mês atual.
    """
    agora = datetime.utcnow()
    hoje_inicio = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    semana_inicio = agora - timedelta(days=agora.weekday())
    mes_inicio = agora.replace(day=1, hour=0, minute=0, second=0)

    def contar(inicio, fim=None, **filtros):
        q = db.query(func.count(Chamado.id)).filter(Chamado.created_at >= inicio)
        if fim:
            q = q.filter(Chamado.created_at < fim)
        for k, v in filtros.items():
            q = q.filter(getattr(Chamado, k) == v)
        return q.scalar() or 0

    # Últimas 5 resoluções
    recentes_resolvidos = (
        db.query(Chamado)
        .filter(Chamado.status == "resolvido", Chamado.data_resolucao.isnot(None))
        .order_by(Chamado.data_resolucao.desc())
        .limit(5).all()
    )

    return {
        "titulo": "Zelô — Zeladoria Urbana de Belém",
        "atualizado": agora.isoformat(),
        "hoje": {
            "abertos": contar(hoje_inicio),
            "resolvidos": contar(hoje_inicio, status="resolvido"),
        },
        "semana": {
            "abertos": contar(semana_inicio),
            "resolvidos": contar(semana_inicio, status="resolvido"),
        },
        "mes": {
            "abertos": contar(mes_inicio),
            "resolvidos": contar(mes_inicio, status="resolvido"),
            "taxa_resolucao": round(
                contar(mes_inicio, status="resolvido") / max(contar(mes_inicio), 1) * 100, 1
            ),
        },
        "total_historico": db.query(func.count(Chamado.id)).scalar() or 0,
        "ultimas_resolucoes": [
            {
                "protocolo": c.protocolo,
                "titulo": c.titulo[:60],
                "bairro": c.bairro.nome if c.bairro else "—",
                "resolvido_em": c.data_resolucao.strftime("%d/%m %H:%M") if c.data_resolucao else "",
            }
            for c in recentes_resolvidos
        ],
    }
