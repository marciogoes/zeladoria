"""
Rotas de Secretarias
API para gestão de secretarias municipais
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.secretaria import Secretaria
from pydantic import BaseModel


# Schemas
class SecretariaBase(BaseModel):
    nome: str
    sigla: str
    descricao: str | None = None
    telefone: str | None = None
    email: str | None = None
    site: str | None = None
    endereco: str | None = None
    bairro: str | None = None
    cep: str | None = None
    secretario: str | None = None
    telefone_secretario: str | None = None
    horario_funcionamento: str | None = None
    cor_primaria: str = "#0066CC"
    icone: str | None = None
    ativo: bool = True


class SecretariaCreate(SecretariaBase):
    pass


class SecretariaResponse(SecretariaBase):
    id: int
    
    class Config:
        from_attributes = True


router = APIRouter(prefix="/api/secretarias")


@router.get("/", response_model=List[SecretariaResponse])
def listar_secretarias(
    skip: int = 0,
    limit: int = 100,
    ativo: bool | None = None,
    db: Session = Depends(get_db)
):
    """Lista todas as secretarias"""
    query = db.query(Secretaria)
    
    if ativo is not None:
        query = query.filter(Secretaria.ativo == ativo)
    
    secretarias = query.offset(skip).limit(limit).all()
    return secretarias


@router.get("/{secretaria_id}", response_model=SecretariaResponse)
def obter_secretaria(secretaria_id: int, db: Session = Depends(get_db)):
    """Obtém detalhes de uma secretaria"""
    secretaria = db.query(Secretaria).filter(Secretaria.id == secretaria_id).first()
    
    if not secretaria:
        raise HTTPException(status_code=404, detail="Secretaria não encontrada")
    
    return secretaria


@router.get("/sigla/{sigla}", response_model=SecretariaResponse)
def obter_secretaria_por_sigla(sigla: str, db: Session = Depends(get_db)):
    """Obtém secretaria pela sigla (ex: SEURB)"""
    secretaria = db.query(Secretaria).filter(Secretaria.sigla == sigla.upper()).first()
    
    if not secretaria:
        raise HTTPException(status_code=404, detail="Secretaria não encontrada")
    
    return secretaria


@router.post("/", response_model=SecretariaResponse)
def criar_secretaria(secretaria: SecretariaCreate, db: Session = Depends(get_db)):
    """Cria uma nova secretaria"""
    # Verificar se sigla já existe
    existe = db.query(Secretaria).filter(Secretaria.sigla == secretaria.sigla.upper()).first()
    if existe:
        raise HTTPException(status_code=400, detail="Sigla já cadastrada")
    
    nova_secretaria = Secretaria(**secretaria.dict())
    nova_secretaria.sigla = nova_secretaria.sigla.upper()
    
    db.add(nova_secretaria)
    db.commit()
    db.refresh(nova_secretaria)
    
    return nova_secretaria


@router.put("/{secretaria_id}", response_model=SecretariaResponse)
def atualizar_secretaria(
    secretaria_id: int,
    secretaria: SecretariaBase,
    db: Session = Depends(get_db)
):
    """Atualiza dados de uma secretaria"""
    db_secretaria = db.query(Secretaria).filter(Secretaria.id == secretaria_id).first()
    
    if not db_secretaria:
        raise HTTPException(status_code=404, detail="Secretaria não encontrada")
    
    for campo, valor in secretaria.dict().items():
        setattr(db_secretaria, campo, valor)
    
    db.commit()
    db.refresh(db_secretaria)
    
    return db_secretaria


@router.delete("/{secretaria_id}")
def deletar_secretaria(secretaria_id: int, db: Session = Depends(get_db)):
    """Deleta uma secretaria"""
    secretaria = db.query(Secretaria).filter(Secretaria.id == secretaria_id).first()
    
    if not secretaria:
        raise HTTPException(status_code=404, detail="Secretaria não encontrada")
    
    db.delete(secretaria)
    db.commit()
    
    return {"message": "Secretaria deletada com sucesso"}
