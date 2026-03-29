from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.database.database import get_db
from app.models.comentario import Comentario
from app.models.chamado import Chamado
from app.models.usuario import Usuario
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/chamados/{chamado_id}/comentarios")

# ============= SCHEMAS =============

class ComentarioCreate(BaseModel):
    comentario: str
    tipo: str = "atualizacao"  # atualizacao, observacao, resolucao
    visivel_cidadao: bool = True

class ComentarioResponse(BaseModel):
    id: int
    chamado_id: int
    usuario_id: int
    usuario_nome: str
    usuario_tipo: str
    comentario: str
    tipo: str
    visivel_cidadao: bool
    data_criacao: str

    class Config:
        from_attributes = True

# ============= ENDPOINTS =============

@router.post("", response_model=dict)
def adicionar_comentario(
    chamado_id: int,
    comentario_data: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Adicionar comentário a um chamado
    
    Tipos de comentário:
    - atualizacao: Atualização sobre o andamento
    - observacao: Observação/nota interna ou externa
    - resolucao: Comentário sobre a resolução
    
    Permissões:
    - Equipe, Gestor, Secretaria, Admin: podem comentar
    - Cidadão: pode comentar no próprio chamado
    """
    
    # Verificar se chamado existe
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    
    # Verificar permissões
    if current_user.tipo == "cidadao" and chamado.usuario_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Você só pode comentar em seus próprios chamados"
        )
    
    # Criar comentário
    novo_comentario = Comentario(
        chamado_id=chamado_id,
        usuario_id=current_user.id,
        comentario=comentario_data.comentario,
        tipo=comentario_data.tipo,
        visivel_cidadao=1 if comentario_data.visivel_cidadao else 0
    )
    
    db.add(novo_comentario)
    db.commit()
    db.refresh(novo_comentario)
    
    return {
        "success": True,
        "message": "Comentário adicionado com sucesso",
        "comentario": novo_comentario.to_dict()
    }

@router.get("", response_model=List[ComentarioResponse])
def listar_comentarios(
    chamado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar todos os comentários de um chamado
    
    Regras de visibilidade:
    - Cidadão: vê apenas comentários com visivel_cidadao=True
    - Equipe/Gestor/Secretaria/Admin: vê todos os comentários
    """
    
    # Verificar se chamado existe
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    
    # Buscar comentários
    query = db.query(Comentario).filter(Comentario.chamado_id == chamado_id)
    
    # Filtrar por visibilidade se for cidadão
    if current_user.tipo == "cidadao":
        query = query.filter(Comentario.visivel_cidadao == 1)
    
    comentarios = query.order_by(Comentario.data_criacao.asc()).all()
    
    # Converter para resposta
    return [
        ComentarioResponse(
            id=c.id,
            chamado_id=c.chamado_id,
            usuario_id=c.usuario_id,
            usuario_nome=c.usuario.nome if c.usuario else "Sistema",
            usuario_tipo=c.usuario.tipo if c.usuario else "sistema",
            comentario=c.comentario,
            tipo=c.tipo,
            visivel_cidadao=bool(c.visivel_cidadao),
            data_criacao=c.data_criacao.isoformat() if c.data_criacao else None
        )
        for c in comentarios
    ]

@router.delete("/{comentario_id}")
def deletar_comentario(
    chamado_id: int,
    comentario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Deletar um comentário
    
    Permissões:
    - Admin: pode deletar qualquer comentário
    - Gestor: pode deletar comentários do próprio setor
    - Usuário: pode deletar apenas seus próprios comentários (até 30 min)
    """
    
    comentario = db.query(Comentario).filter(
        Comentario.id == comentario_id,
        Comentario.chamado_id == chamado_id
    ).first()
    
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    # Verificar permissões
    pode_deletar = False
    
    if current_user.tipo == "admin":
        pode_deletar = True
    elif current_user.tipo == "gestor":
        pode_deletar = True  # Gestor pode deletar qualquer comentário
    elif comentario.usuario_id == current_user.id:
        # Usuário pode deletar seu próprio comentário apenas se for recente
        tempo_decorrido = (datetime.utcnow() - comentario.data_criacao).total_seconds()
        if tempo_decorrido <= 1800:  # 30 minutos
            pode_deletar = True
        else:
            raise HTTPException(
                status_code=403,
                detail="Você só pode deletar comentários até 30 minutos após a criação"
            )
    
    if not pode_deletar:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para deletar este comentário"
        )
    
    db.delete(comentario)
    db.commit()
    
    return {"success": True, "message": "Comentário deletado com sucesso"}

@router.patch("/{comentario_id}")
def editar_comentario(
    chamado_id: int,
    comentario_id: int,
    comentario_data: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Editar um comentário existente
    
    Permissões:
    - Usuário pode editar seu próprio comentário (até 30 min)
    - Admin/Gestor podem editar qualquer comentário
    """
    
    comentario = db.query(Comentario).filter(
        Comentario.id == comentario_id,
        Comentario.chamado_id == chamado_id
    ).first()
    
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    # Verificar permissões
    pode_editar = False
    
    if current_user.tipo in ["admin", "gestor"]:
        pode_editar = True
    elif comentario.usuario_id == current_user.id:
        # Usuário pode editar seu próprio comentário apenas se for recente
        tempo_decorrido = (datetime.utcnow() - comentario.data_criacao).total_seconds()
        if tempo_decorrido <= 1800:  # 30 minutos
            pode_editar = True
        else:
            raise HTTPException(
                status_code=403,
                detail="Você só pode editar comentários até 30 minutos após a criação"
            )
    
    if not pode_editar:
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para editar este comentário"
        )
    
    # Atualizar comentário
    comentario.comentario = comentario_data.comentario
    comentario.tipo = comentario_data.tipo
    comentario.visivel_cidadao = 1 if comentario_data.visivel_cidadao else 0
    
    db.commit()
    db.refresh(comentario)
    
    return {
        "success": True,
        "message": "Comentário atualizado com sucesso",
        "comentario": comentario.to_dict()
    }
