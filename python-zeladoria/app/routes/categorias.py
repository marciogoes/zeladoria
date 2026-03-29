from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.utils.auth import get_current_user, require_role
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).filter(Categoria.ativo == True).order_by(Categoria.nome).all()
    return categorias

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(
    categoria_data: CategoriaCreate,
    current_user: Usuario = Depends(require_role("gestor", "admin")),
    db: Session = Depends(get_db)
):
    categoria = Categoria(**categoria_data.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria
