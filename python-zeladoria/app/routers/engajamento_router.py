"""
Sprint 3 & 4 — Votação e Gamificação
Sistema de Zeladoria Urbana - Belém/PA
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, Integer
from typing import List
from datetime import datetime

from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.usuario import Usuario
from app.models.bairro import Bairro
from app.models.gamificacao import VotoChamado, PontosUsuario, ConquistaUsuario
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/engajamento", tags=["Engajamento"])

# ──────────────────────────────────────────────
# CONSTANTES DE PONTUAÇÃO
# ──────────────────────────────────────────────
PTS = {
    "abrir_chamado":    10,
    "votar":             2,
    "avaliar":           5,
    "chamado_resolvido":15,
}

NIVEIS = [
    (0,   "iniciante",   "🌱"),
    (50,  "colaborador", "⭐"),
    (150, "guardião",    "🛡️"),
    (350, "zelador",     "🏅"),
    (700, "mestre",      "👑"),
]

CONQUISTAS = [
    ("primeiro_chamado",   "🎯", "Abriu o primeiro chamado"),
    ("5_chamados",         "📋", "5 chamados abertos"),
    ("20_chamados",        "🔥", "20 chamados — cidadão ativo"),
    ("primeiro_voto",      "👍", "Deu o primeiro upvote"),
    ("10_votos",           "💪", "10 upvotes dados"),
    ("primeira_avaliacao", "⭐", "Avaliou o primeiro chamado"),
]


def calcular_nivel(pontos: int) -> tuple:
    nivel = NIVEIS[0]
    for item in NIVEIS:
        if pontos >= item[0]:
            nivel = item
    return nivel  # (limite, nome, icone)


def get_ou_criar_pontos(db: Session, usuario_id: int) -> PontosUsuario:
    pts = db.query(PontosUsuario).filter_by(usuario_id=usuario_id).first()
    if not pts:
        pts = PontosUsuario(usuario_id=usuario_id)
        db.add(pts)
        db.commit()
        db.refresh(pts)
    return pts


def verificar_conquistas(db: Session, usuario_id: int, pts: PontosUsuario) -> List[dict]:
    """Verifica e desbloqueia novas conquistas. Retorna lista das novas."""
    novas = []
    existentes = {c.conquista for c in db.query(ConquistaUsuario).filter_by(usuario_id=usuario_id).all()}

    checks = [
        ("primeiro_chamado",   pts.chamados_abertos >= 1),
        ("5_chamados",         pts.chamados_abertos >= 5),
        ("20_chamados",        pts.chamados_abertos >= 20),
        ("primeiro_voto",      pts.votos_dados >= 1),
        ("10_votos",           pts.votos_dados >= 10),
        ("primeira_avaliacao", pts.avaliacoes_feitas >= 1),
    ]

    for codigo, condicao in checks:
        if condicao and codigo not in existentes:
            info = next((c for c in CONQUISTAS if c[0] == codigo), None)
            if info:
                nova = ConquistaUsuario(
                    usuario_id=usuario_id,
                    conquista=codigo,
                    icone=info[1],
                    descricao=info[2],
                )
                db.add(nova)
                novas.append({"conquista": codigo, "icone": info[1], "descricao": info[2]})

    if novas:
        db.commit()
    return novas


def adicionar_pontos(db: Session, usuario_id: int, acao: str) -> List[dict]:
    """Adiciona pontos e verifica conquistas."""
    pts = get_ou_criar_pontos(db, usuario_id)
    pts.total_pontos += PTS.get(acao, 0)

    if acao == "abrir_chamado":
        pts.chamados_abertos += 1
    elif acao == "votar":
        pts.votos_dados += 1
    elif acao == "avaliar":
        pts.avaliacoes_feitas += 1

    _, nivel, _ = calcular_nivel(pts.total_pontos)
    pts.nivel = nivel
    pts.atualizado_em = datetime.utcnow()
    db.commit()

    return verificar_conquistas(db, usuario_id, pts)


# ──────────────────────────────────────────────
# ENDPOINTS — VOTAÇÃO
# ──────────────────────────────────────────────

@router.post("/chamados/{chamado_id}/votar")
def votar_chamado(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upvote num chamado — toggle. Um cidadão, um voto."""
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")

    if chamado.usuario_id == current_user.id:
        raise HTTPException(400, "Você não pode votar no seu próprio chamado")

    voto_existente = db.query(VotoChamado).filter_by(
        usuario_id=current_user.id, chamado_id=chamado_id
    ).first()

    if voto_existente:
        db.delete(voto_existente)
        chamado.total_votos = max(0, (chamado.total_votos or 0) - 1)
        db.commit()
        return {"votou": False, "total_votos": chamado.total_votos}

    try:
        voto = VotoChamado(usuario_id=current_user.id, chamado_id=chamado_id)
        db.add(voto)
        chamado.total_votos = (chamado.total_votos or 0) + 1
        db.commit()
        novas_conquistas = adicionar_pontos(db, current_user.id, "votar")
        return {"votou": True, "total_votos": chamado.total_votos, "novas_conquistas": novas_conquistas}
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Já votou neste chamado")


@router.get("/chamados/{chamado_id}/votos")
def ver_votos(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")

    meu_voto = db.query(VotoChamado).filter_by(
        usuario_id=current_user.id, chamado_id=chamado_id
    ).first()

    return {"total_votos": chamado.total_votos or 0, "meu_voto": bool(meu_voto)}


# ──────────────────────────────────────────────
# ENDPOINTS — GAMIFICAÇÃO
# ──────────────────────────────────────────────

@router.get("/meu-perfil")
def meu_perfil_gamificacao(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pts = get_ou_criar_pontos(db, current_user.id)
    conquistas = db.query(ConquistaUsuario).filter_by(usuario_id=current_user.id).all()
    _, nivel, icone_nivel = calcular_nivel(pts.total_pontos)

    proximo = None
    for limite, nome, icone in NIVEIS:
        if pts.total_pontos < limite:
            proximo = {"nome": nome, "pontos_necessarios": limite - pts.total_pontos}
            break

    return {
        "usuario": {"id": current_user.id, "nome": current_user.nome, "tipo": current_user.tipo},
        "pontos": pts.total_pontos,
        "nivel": nivel,
        "icone_nivel": icone_nivel,
        "chamados_abertos": pts.chamados_abertos,
        "votos_dados": pts.votos_dados,
        "avaliacoes_feitas": pts.avaliacoes_feitas,
        "proximo_nivel": proximo,
        "conquistas": [
            {
                "conquista": c.conquista,
                "icone": c.icone,
                "descricao": c.descricao,
                "data": c.desbloqueada_em.isoformat() if c.desbloqueada_em else None,
            }
            for c in conquistas
        ],
    }


@router.get("/ranking")
def ranking_cidadaos(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Top cidadãos por pontuação."""
    ranking = (
        db.query(PontosUsuario, Usuario)
        .join(Usuario, PontosUsuario.usuario_id == Usuario.id)
        .filter(Usuario.tipo == "cidadao")
        .order_by(PontosUsuario.total_pontos.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "posicao": i + 1,
            "nome": u.nome,
            "pontos": p.total_pontos,
            "nivel": p.nivel,
            "chamados_abertos": p.chamados_abertos,
        }
        for i, (p, u) in enumerate(ranking)
    ]


@router.get("/ranking-bairros")
def ranking_bairros(db: Session = Depends(get_db)):
    """Bairros com mais chamados — ranking de zeladoria."""
    resultado = (
        db.query(
            Bairro.nome,
            Bairro.regiao,
            func.count(Chamado.id).label("total"),
        )
        .join(Chamado, Chamado.bairro_id == Bairro.id, isouter=True)
        .group_by(Bairro.id)
        .order_by(func.count(Chamado.id).desc())
        .limit(10)
        .all()
    )

    return [
        {"bairro": r.nome, "regiao": r.regiao, "total_chamados": r.total}
        for r in resultado
    ]


@router.post("/chamados/{chamado_id}/pontos-abertura")
def registrar_pontos_abertura(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Chamado após criar — registra pontos de abertura."""
    novas_conquistas = adicionar_pontos(db, current_user.id, "abrir_chamado")
    pts = get_ou_criar_pontos(db, current_user.id)
    return {
        "pontos_ganhos": PTS["abrir_chamado"],
        "total_pontos": pts.total_pontos,
        "nivel": pts.nivel,
        "novas_conquistas": novas_conquistas,
    }
