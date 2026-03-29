from pydantic import BaseModel, ConfigDict
from typing import Optional

class BairroBase(BaseModel):
    nome: str
    regiao: Optional[str] = None

class BairroCreate(BairroBase):
    pass

class BairroResponse(BairroBase):
    id: int
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
