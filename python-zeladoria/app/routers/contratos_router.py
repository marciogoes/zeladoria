"""
Sprint 7 — Contratos de Fornecedores + LGPD
"""
from typing import Optional, List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
import re

from app.database.database import get_db
from app.models.sprints_5_8 import Fornecedor, ContratoFornecedor, SolicitacaoLGPD
from app.models.usuario import Usuario
from app.utils.auth import get_current_user, require_role, revoke_token
from app.utils.auditoria import registrar

router = APIRouter(prefix="/api/contratos", tags=["Contratos & LGPD"])


# ─────────────────────────────────────────
# FORNECEDORES
# ─────────────────────────────────────────
class FornecedorCreate(BaseModel):
    nome: str
    cnpj: str
    email: Optional[str] = None
    telefone: Optional[str] = None

    @field_validator("cnpj")
    @classmethod
    def validar_cnpj(cls, v: str) -> str:
        """Valida formato e dígito verificador do CNPJ."""
        digits = re.sub(r"\D", "", v)
        if len(digits) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        if len(set(digits)) == 1:
            raise ValueError("CNPJ inválido")

        def calc(d, weights):
            s = sum(int(d[i]) * weights[i] for i in range(len(weights)))
            r = s % 11
            return 0 if r < 2 else 11 - r

        w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        if calc(digits, w1) != int(digits[12]) or calc(digits, w2) != int(digits[13]):
            raise ValueError("CNPJ com dígito verificador inválido")
        # Formata: XX.XXX.XXX/XXXX-XX
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"


@router.get("/fornecedores", dependencies=[Depends(require_role("admin", "gestor"))])
def listar_fornecedores(db: Session = Depends(get_db)):
    forn = db.query(Fornecedor).filter(Fornecedor.ativo == True).all()
    return [{"id": f.id, "nome": f.nome, "cnpj": f.cnpj, "email": f.email} for f in forn]


@router.post("/fornecedores", dependencies=[Depends(require_role("admin", "gestor"))])
def criar_fornecedor(dados: FornecedorCreate, db: Session = Depends(get_db)):
    if db.query(Fornecedor).filter_by(cnpj=dados.cnpj).first():
        raise HTTPException(400, "CNPJ já cadastrado")
    f = Fornecedor(**dados.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    return {"id": f.id, "nome": f.nome}


# ─────────────────────────────────────────
# CONTRATOS
# ─────────────────────────────────────────
class ContratoCreate(BaseModel):
    fornecedor_id: int
    secretaria_id: Optional[int] = None
    numero: str
    objeto: Optional[str] = None
    valor: Optional[float] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    sla_horas: int = 48


@router.get("/", dependencies=[Depends(require_role("admin", "gestor"))])
def listar_contratos(db: Session = Depends(get_db)):
    contratos = db.query(ContratoFornecedor).all()
    return [
        {
            "id": c.id,
            "numero": c.numero,
            "fornecedor": c.fornecedor.nome if c.fornecedor else None,
            "objeto": c.objeto,
            "valor": c.valor,
            "status": c.status,
            "nota_desempenho": c.nota_desempenho,
            "total_chamados": c.total_chamados,
            "chamados_no_prazo": c.chamados_no_prazo,
            "sla_horas": c.sla_horas,
            "data_fim": c.data_fim.isoformat() if c.data_fim else None,
        }
        for c in contratos
    ]


@router.post("/")
def criar_contrato(
    dados: ContratoCreate,
    current_user: Usuario = Depends(require_role("admin", "gestor")),
    db: Session = Depends(get_db),
):
    if db.query(ContratoFornecedor).filter_by(numero=dados.numero).first():
        raise HTTPException(400, "Número de contrato já existe")
    c = ContratoFornecedor(**dados.model_dump())
    db.add(c)
    db.flush()
    registrar(db, "Contrato", c.id, "criado", {"numero": c.numero}, current_user.id)
    db.commit()
    return {"id": c.id, "numero": c.numero}


@router.get("/{contrato_id}/desempenho", dependencies=[Depends(require_role("admin", "gestor"))])
def desempenho_contrato(contrato_id: int, db: Session = Depends(get_db)):
    c = db.query(ContratoFornecedor).filter_by(id=contrato_id).first()
    if not c:
        raise HTTPException(404, "Contrato não encontrado")
    taxa = round(c.chamados_no_prazo / c.total_chamados * 100, 1) if c.total_chamados else 0
    return {
        "numero": c.numero,
        "fornecedor": c.fornecedor.nome if c.fornecedor else None,
        "total_chamados": c.total_chamados,
        "chamados_no_prazo": c.chamados_no_prazo,
        "taxa_cumprimento_sla": taxa,
        "nota_desempenho": c.nota_desempenho,
        "alerta_baixo_desempenho": taxa < 70,
    }


# ─────────────────────────────────────────
# LGPD
# ─────────────────────────────────────────
class LGPDRequest(BaseModel):
    tipo: str  # exportar | anonimizar | excluir

@router.post("/lgpd/solicitar")
def solicitar_lgpd(
    payload: LGPDRequest,
    request: Request,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tipo = payload.tipo
    if tipo not in ("exportar", "anonimizar", "excluir"):
        raise HTTPException(400, "Tipo inválido. Use: exportar, anonimizar ou excluir")

    sol = SolicitacaoLGPD(usuario_id=current_user.id, tipo=tipo)
    db.add(sol)
    db.commit()
    db.refresh(sol)

    if tipo == "exportar":
        from app.models.chamado import Chamado as ChamadoModel
        chamados = db.query(ChamadoModel).filter_by(usuario_id=current_user.id).all()
        return {
            "solicitacao_id": sol.id,
            "tipo": tipo,
            "dados": {
                "nome": current_user.nome,
                "email": current_user.email,
                "telefone": current_user.telefone,
                "total_chamados": len(chamados),
                "chamados": [
                    {"protocolo": c.protocolo, "titulo": c.titulo, "status": c.status, "criado_em": str(c.created_at)}
                    for c in chamados
                ],
            },
        }

    agora = datetime.now(timezone.utc)

    if tipo == "anonimizar":
        current_user.nome = f"Cidadão Anônimo #{current_user.id}"
        current_user.telefone = None
        current_user.cpf = None
        sol.status = "concluida"
        sol.concluido_em = agora
        db.commit()
        return {"solicitacao_id": sol.id, "tipo": tipo, "msg": "Dados pessoais anonimizados com sucesso."}

    if tipo == "excluir":
        # Revoga o token JWT imediatamente (não espera os 8h expirarem)
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            revoke_token(auth_header[7:].strip())

        current_user.ativo = False
        current_user.nome = f"Conta Excluída #{current_user.id}"
        current_user.email = f"excluido_{current_user.id}@zelo.app"
        current_user.telefone = None
        current_user.cpf = None
        sol.status = "concluida"
        sol.concluido_em = agora
        db.commit()
        return {"solicitacao_id": sol.id, "tipo": tipo, "msg": "Conta removida e sesso encerrada. Dados pessoais excluídos conforme LGPD."}

    return {"solicitacao_id": sol.id, "status": "pendente"}
