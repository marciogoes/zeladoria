"""
Sprint 16 — Endpoints de Onboarding e Configuração Inicial
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.usuario import Usuario
from app.models.chamado import Chamado
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/onboarding", tags=["Onboarding"])

PASSOS_ONBOARDING = [
    {
        "id": 1,
        "titulo": "Bem-vindo ao Zelô!",
        "descricao": "O Zelô conecta cidadãos e a Prefeitura de Belém para resolver problemas urbanos mais rápido.",
        "acao": None,
        "icone": "🏛️",
    },
    {
        "id": 2,
        "titulo": "Abra seu primeiro chamado",
        "descricao": "Encontrou um buraco, lixo acumulado ou lâmpada queimada? Registre agora em segundos.",
        "acao": {"label": "Abrir Chamado", "tab": "novo-chamado"},
        "icone": "📋",
    },
    {
        "id": 3,
        "titulo": "Apoie chamados do seu bairro",
        "descricao": "Dê upvote em problemas relatados por outros cidadãos — quanto mais votos, maior a prioridade.",
        "acao": {"label": "Ver Chamados", "tab": "chamados"},
        "icone": "👍",
    },
    {
        "id": 4,
        "titulo": "Ganhe pontos e conquistas",
        "descricao": "Cada ação no Zelô rende pontos. Suba de nível e vire um Guardião ou Mestre do seu bairro!",
        "acao": {"label": "Ver Perfil", "tab": "perfil"},
        "icone": "🏆",
    },
    {
        "id": 5,
        "titulo": "Vote em obras para o seu bairro",
        "descricao": "Participe do orçamento participativo e ajude a decidir quais obras a Prefeitura vai priorizar.",
        "acao": {"label": "Ver Propostas", "tab": "propostas"},
        "icone": "🗳️",
    },
]


@router.get("/passos")
def passos_onboarding(current_user: Usuario = Depends(get_current_user)):
    """Retorna os passos de onboarding com progresso do usuário."""
    from app.models.gamificacao import PontosUsuario

    return {
        "usuario": {"nome": current_user.nome, "tipo": current_user.tipo},
        "passos": PASSOS_ONBOARDING,
        "total": len(PASSOS_ONBOARDING),
    }


@router.get("/checklist")
def checklist_onboarding(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Verifica quais passos do onboarding o usuário já completou."""
    from app.models.gamificacao import PontosUsuario, VotoChamado

    pts_rec = db.query(PontosUsuario).filter_by(usuario_id=current_user.id).first()

    tem_chamado = db.query(func.count(Chamado.id)).filter_by(
        usuario_id=current_user.id
    ).scalar() > 0

    tem_voto = db.query(func.count(VotoChamado.id)).filter_by(
        usuario_id=current_user.id
    ).scalar() > 0

    concluidos = []
    if True:        concluidos.append(1)   # Sempre — só por entrar
    if tem_chamado: concluidos.append(2)
    if tem_voto:    concluidos.append(3)
    if pts_rec and pts_rec.total_pontos >= 10: concluidos.append(4)
    if pts_rec and pts_rec.total_pontos >= 20: concluidos.append(5)

    pct = round(len(concluidos) / len(PASSOS_ONBOARDING) * 100)

    return {
        "concluidos": concluidos,
        "pendentes": [p for p in range(1, len(PASSOS_ONBOARDING)+1) if p not in concluidos],
        "percentual": pct,
        "completo": pct == 100,
    }


@router.get("/estatisticas-boas-vindas")
def estatisticas_boas_vindas(db: Session = Depends(get_db)):
    """Dados para a tela de boas-vindas e landing."""
    total = db.query(func.count(Chamado.id)).scalar() or 0
    resolvidos = db.query(func.count(Chamado.id)).filter(
        Chamado.status == "resolvido"
    ).scalar() or 0
    categorias = db.query(func.count(Categoria.id)).scalar() or 0
    bairros = db.query(func.count(Bairro.id)).scalar() or 0

    return {
        "total_chamados": total,
        "chamados_resolvidos": resolvidos,
        "taxa_resolucao": round(resolvidos / total * 100, 1) if total else 0,
        "categorias_cobertas": categorias,
        "bairros_ativos": bairros,
        "mensagem": f"Juntos já resolvemos {resolvidos} problemas em Belém!",
    }
