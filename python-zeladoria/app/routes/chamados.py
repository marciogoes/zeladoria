from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database.database import get_db
from app.models.chamado import Chamado
from app.models.usuario import Usuario
from app.schemas.chamado import ChamadoCreate, ChamadoResponse, ChamadoUpdate, ChamadoAvaliar
from app.utils.auth import get_current_user
from app.utils.upload import save_upload_file
from pydantic import BaseModel

router = APIRouter()

# Schema para reclassificação
class ReclassificarChamado(BaseModel):
    servico_codigo: str
    servico_nome: str
    categoria: str
    sla_horas: int
    prioridade: str

@router.get("/", response_model=List[ChamadoResponse])
def listar_chamados(
    status: Optional[str] = None,
    prioridade: Optional[str] = None,
    categoria_id: Optional[int] = None,
    bairro_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Chamado)
    
    # Filtros
    if status:
        query = query.filter(Chamado.status == status)
    if prioridade:
        query = query.filter(Chamado.prioridade == prioridade)
    if categoria_id:
        query = query.filter(Chamado.categoria_id == categoria_id)
    if bairro_id:
        query = query.filter(Chamado.bairro_id == bairro_id)
    if search:
        query = query.filter(
            (Chamado.protocolo.like(f"%{search}%")) |
            (Chamado.titulo.like(f"%{search}%"))
        )
    
    # Cidadão só vê seus chamados
    if current_user.tipo == "cidadao":
        query = query.filter(Chamado.usuario_id == current_user.id)
    
    chamados = query.order_by(Chamado.created_at.desc()).all()
    return chamados

@router.get("/{chamado_id}", response_model=ChamadoResponse)
def obter_chamado(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    # Cidadão só vê seus chamados
    if current_user.tipo == "cidadao" and chamado.usuario_id != current_user.id:
        raise HTTPException(403, "Sem permissão")
    
    return chamado

@router.post("/", response_model=ChamadoResponse, status_code=status.HTTP_201_CREATED)
async def criar_chamado(
    titulo: str = Form(...),
    descricao: str = Form(...),
    endereco: str = Form(...),
    categoria_id: int = Form(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    bairro_id: Optional[int] = Form(None),
    prioridade: Optional[str] = Form('media'),  # Padrão: média
    foto: Optional[UploadFile] = File(None),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Upload da foto
    foto_path = None
    if foto:
        foto_path = await save_upload_file(foto)
    
    # Criar chamado
    chamado = Chamado(
        titulo=titulo,
        descricao=descricao,
        endereco=endereco,
        latitude=latitude,
        longitude=longitude,
        categoria_id=categoria_id,
        bairro_id=bairro_id,
        prioridade=prioridade,  # Sempre começa como 'media'
        foto_antes=foto_path,
        usuario_id=current_user.id
    )
    
    db.add(chamado)
    db.commit()
    db.refresh(chamado)
    
    return chamado

@router.put("/{chamado_id}", response_model=ChamadoResponse)
async def atualizar_chamado(
    chamado_id: int,
    chamado_data: ChamadoUpdate,
    foto: Optional[UploadFile] = File(None),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    # Cidadão não pode atualizar
    if current_user.tipo == "cidadao":
        raise HTTPException(403, "Sem permissão para atualizar")
    
    # Atualizar campos
    if chamado_data.status:
        chamado.status = chamado_data.status
        if chamado_data.status == "resolvido":
            chamado.data_resolucao = datetime.utcnow()
    
    if chamado_data.prioridade:
        chamado.prioridade = chamado_data.prioridade
    
    if chamado_data.responsavel_id:
        chamado.responsavel_id = chamado_data.responsavel_id
    
    # Upload foto depois
    if foto:
        chamado.foto_depois = await save_upload_file(foto)
    
    chamado.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(chamado)
    
    return chamado

@router.post("/{chamado_id}/avaliar", response_model=ChamadoResponse)
def avaliar_chamado(
    chamado_id: int,
    avaliacao_data: ChamadoAvaliar,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    # Apenas o criador pode avaliar
    if chamado.usuario_id != current_user.id:
        raise HTTPException(403, "Sem permissão")
    
    # Apenas resolvidos podem ser avaliados
    if chamado.status != "resolvido":
        raise HTTPException(400, "Apenas chamados resolvidos podem ser avaliados")
    
    chamado.avaliacao = avaliacao_data.avaliacao
    chamado.comentario_avaliacao = avaliacao_data.comentario_avaliacao
    
    db.commit()
    db.refresh(chamado)
    
    return chamado

@router.patch("/{chamado_id}/status", response_model=ChamadoResponse)
def atualizar_status(
    chamado_id: int,
    status_data: dict,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    # Cidadão não pode atualizar status
    if current_user.tipo == "cidadao":
        raise HTTPException(403, "Sem permissão")
    
    novo_status = status_data.get('status')
    if novo_status:
        chamado.status = novo_status
        if novo_status == "resolvido":
            chamado.data_resolucao = datetime.utcnow()
        chamado.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(chamado)
    
    return chamado

@router.patch("/{chamado_id}/prioridade", response_model=ChamadoResponse)
def atualizar_prioridade(
    chamado_id: int,
    prioridade_data: dict,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    # Apenas secretaria, gestor e admin podem definir prioridade
    if current_user.tipo not in ["secretaria", "gestor", "admin", "equipe"]:
        raise HTTPException(403, "Sem permissão")
    
    nova_prioridade = prioridade_data.get('prioridade')
    if nova_prioridade:
        chamado.prioridade = nova_prioridade
        chamado.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(chamado)
    
    return chamado

# ============================================================================
# NOVO: RECLASSIFICAR CHAMADO
# ============================================================================

@router.patch("/{chamado_id}/reclassificar", response_model=ChamadoResponse)
def reclassificar_chamado(
    chamado_id: int,
    reclassificacao: ReclassificarChamado,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reclassifica um chamado com base em um serviço do catálogo
    
    Atualiza:
    - Categoria do chamado
    - Prioridade
    - SLA (prazo de atendimento)
    - Adiciona observação sobre a reclassificação
    """
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    # Apenas secretaria, gestor e admin podem reclassificar
    if current_user.tipo not in ["secretaria", "gestor", "admin"]:
        raise HTTPException(403, "Sem permissão para reclassificar")
    
    # Guardar categoria anterior para histórico
    categoria_anterior = chamado.categoria.nome if chamado.categoria else "Sem categoria"
    prioridade_anterior = chamado.prioridade
    
    # Atualizar chamado com dados do serviço
    chamado.prioridade = reclassificacao.prioridade
    chamado.updated_at = datetime.utcnow()
    
    # Adicionar observação na descrição
    observacao = f"\n\n--- RECLASSIFICADO ---\n"
    observacao += f"Data: {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}\n"
    observacao += f"Por: {current_user.nome}\n"
    observacao += f"Serviço: {reclassificacao.servico_codigo} - {reclassificacao.servico_nome}\n"
    observacao += f"Categoria anterior: {categoria_anterior}\n"
    observacao += f"Nova categoria: {reclassificacao.categoria}\n"
    observacao += f"Prioridade anterior: {prioridade_anterior}\n"
    observacao += f"Nova prioridade: {reclassificacao.prioridade}\n"
    observacao += f"SLA: {reclassificacao.sla_horas}h\n"
    
    if not chamado.descricao.endswith("--- RECLASSIFICADO ---"):
        chamado.descricao += observacao
    
    db.commit()
    db.refresh(chamado)
    
    return chamado

@router.delete("/{chamado_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_chamado(
    chamado_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Apenas admin pode deletar
    if current_user.tipo not in ["admin", "gestor"]:
        raise HTTPException(403, "Sem permissão")
    
    chamado = db.query(Chamado).filter(Chamado.id == chamado_id).first()
    
    if not chamado:
        raise HTTPException(404, "Chamado não encontrado")
    
    db.delete(chamado)
    db.commit()
    
    return None
