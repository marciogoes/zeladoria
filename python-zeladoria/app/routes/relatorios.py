from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.models.usuario import Usuario
from app.utils.auth import require_role

router = APIRouter()

@router.get("/dashboard")
def obter_dashboard(
    current_user: Usuario = Depends(require_role("gestor", "admin", "secretaria", "equipe")),
    db: Session = Depends(get_db)
):
    # Total de chamados
    total_chamados = db.query(func.count(Chamado.id)).scalar()
    
    # Chamados por status
    por_status = db.query(
        Chamado.status,
        func.count(Chamado.id).label("total")
    ).group_by(Chamado.status).all()
    
    # Chamados por prioridade
    por_prioridade = db.query(
        Chamado.prioridade,
        func.count(Chamado.id).label("total")
    ).group_by(Chamado.prioridade).all()
    
    # Top 5 categorias
    top_categorias = db.query(
        Categoria.id,
        Categoria.nome,
        Categoria.icone,
        Categoria.cor,
        func.count(Chamado.id).label("total")
    ).join(Chamado, Chamado.categoria_id == Categoria.id)\
     .group_by(Categoria.id)\
     .order_by(func.count(Chamado.id).desc())\
     .limit(5).all()
    
    # Top 5 bairros
    top_bairros = db.query(
        Bairro.id,
        Bairro.nome,
        func.count(Chamado.id).label("total")
    ).join(Chamado, Chamado.bairro_id == Bairro.id)\
     .group_by(Bairro.id)\
     .order_by(func.count(Chamado.id).desc())\
     .limit(5).all()
    
    # Chamados recentes
    recentes = db.query(Chamado)\
        .order_by(Chamado.created_at.desc())\
        .limit(10).all()
    
    # Média de avaliação
    avaliacao_media = db.query(func.avg(Chamado.avaliacao))\
        .filter(Chamado.avaliacao.isnot(None))\
        .scalar() or 0
    
    return {
        "total_chamados": total_chamados,
        "por_status": [{"status": s, "total": t} for s, t in por_status],
        "por_prioridade": [{"prioridade": p, "total": t} for p, t in por_prioridade],
        "top_categorias": [
            {
                "categoria": {
                    "id": c.id,
                    "nome": c.nome,
                    "icone": c.icone,
                    "cor": c.cor
                },
                "total": c.total
            } for c in top_categorias
        ],
        "top_bairros": [
            {
                "bairro": {
                    "id": b.id,
                    "nome": b.nome
                },
                "total": b.total
            } for b in top_bairros
        ],
        "recentes": recentes,
        "avaliacao_media": round(float(avaliacao_media), 1)
    }
