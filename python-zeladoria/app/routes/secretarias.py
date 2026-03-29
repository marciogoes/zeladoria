"""
Rotas de Secretarias
API para gestão de secretarias municipais
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models.secretaria import Secretaria
from app.utils.auth import require_role
from app.models.usuario import Usuario
from pydantic import BaseModel, ConfigDict


class SecretariaBase(BaseModel):
    nome: str
    sigla: str
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    site: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    secretario: Optional[str] = None
    telefone_secretario: Optional[str] = None
    horario_funcionamento: Optional[str] = None
    cor_primaria: str = "#0066CC"
    icone: Optional[str] = None
    ativo: bool = True


class SecretariaCreate(SecretariaBase):
    pass


class SecretariaResponse(SecretariaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


router = APIRouter(prefix="/api/secretarias")


@router.get("/", response_model=List[SecretariaResponse])
def listar_secretarias(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Secretaria)
    if ativo is not None:
        query = query.filter(Secretaria.ativo == ativo)
    return query.offset(skip).limit(limit).all()


@router.get("/{secretaria_id}", response_model=SecretariaResponse)
def obter_secretaria(secretaria_id: int, db: Session = Depends(get_db)):
    s = db.query(Secretaria).filter(Secretaria.id == secretaria_id).first()
    if not s:
        raise HTTPException(404, "Secretaria não encontrada")
    return s


@router.get("/sigla/{sigla}", response_model=SecretariaResponse)
def obter_secretaria_por_sigla(sigla: str, db: Session = Depends(get_db)):
    s = db.query(Secretaria).filter(Secretaria.sigla == sigla.upper()).first()
    if not s:
        raise HTTPException(404, "Secretaria não encontrada")
    return s


@router.post("/", response_model=SecretariaResponse)
def criar_secretaria(
    secretaria: SecretariaCreate,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    existe = db.query(Secretaria).filter(Secretaria.sigla == secretaria.sigla.upper()).first()
    if existe:
        raise HTTPException(400, "Sigla já cadastrada")
    dados = secretaria.model_dump()
    dados["sigla"] = dados["sigla"].upper()
    nova = Secretaria(**dados)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.put("/{secretaria_id}", response_model=SecretariaResponse)
def atualizar_secretaria(
    secretaria_id: int,
    secretaria: SecretariaBase,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    db_s = db.query(Secretaria).filter(Secretaria.id == secretaria_id).first()
    if not db_s:
        raise HTTPException(404, "Secretaria não encontrada")
    for campo, valor in secretaria.model_dump().items():
        setattr(db_s, campo, valor)
    db.commit()
    db.refresh(db_s)
    return db_s


@router.delete("/{secretaria_id}")
def deletar_secretaria(
    secretaria_id: int,
    current_user: Usuario = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    s = db.query(Secretaria).filter(Secretaria.id == secretaria_id).first()
    if not s:
        raise HTTPException(404, "Secretaria não encontrada")
    db.delete(s)
    db.commit()
    return {"message": "Secretaria deletada com sucesso"}
