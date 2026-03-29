from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    icone: Optional[str] = None
    cor: str = "#667eea"
    sla_horas: int = 72

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
