from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Schema para criar tarefa
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Schema para atualizar tarefa
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Schema para resposta (inclui id e datas)
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
