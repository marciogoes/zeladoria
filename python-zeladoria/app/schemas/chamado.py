from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.usuario import UsuarioResponse
from app.schemas.categoria import CategoriaResponse
from app.schemas.bairro import BairroResponse

class ChamadoBase(BaseModel):
    titulo: str
    descricao: str
    endereco: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    categoria_id: int
    bairro_id: Optional[int] = None

class ChamadoCreate(ChamadoBase):
    pass

class ChamadoUpdate(BaseModel):
    status: Optional[str] = None
    prioridade: Optional[str] = None
    responsavel_id: Optional[int] = None

class ChamadoAvaliar(BaseModel):
    avaliacao: int
    comentario_avaliacao: Optional[str] = None

class ChamadoResponse(ChamadoBase):
    id: int
    protocolo: str
    foto_antes: Optional[str] = None
    foto_depois: Optional[str] = None
    status: str
    prioridade: str
    avaliacao: Optional[int] = None
    comentario_avaliacao: Optional[str] = None
    data_resolucao: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    usuario_id: int
    responsavel_id: Optional[int] = None
    
    # Votos
    total_votos: Optional[int] = 0

    # Relacionamentos
    usuario: Optional[UsuarioResponse] = None
    responsavel: Optional[UsuarioResponse] = None
    categoria: Optional[CategoriaResponse] = None
    bairro: Optional[BairroResponse] = None

    model_config = ConfigDict(from_attributes=True)
