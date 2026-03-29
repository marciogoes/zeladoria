from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.bairro import Bairro
from app.schemas.bairro import BairroResponse

router = APIRouter()

@router.get("/", response_model=List[BairroResponse])
def listar_bairros(db: Session = Depends(get_db)):
    bairros = db.query(Bairro).filter(Bairro.ativo == True).order_by(Bairro.nome).all()
    return bairros
