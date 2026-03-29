from app.models.usuario import Usuario
from app.models.secretaria import Secretaria
from app.models.categoria import Categoria
from app.models.bairro import Bairro
from app.models.chamado import Chamado
from app.models.comentario import Comentario
from app.models.gamificacao import VotoChamado, PontosUsuario, ConquistaUsuario
from app.models.sprints_5_8 import (
    SensorIoT, LeituraSensor,
    PropostaOrcamento, VotoProposta,
    RegistroAuditoria,
    Fornecedor, ContratoFornecedor,
    SolicitacaoLGPD,
)
from app.models.sprints_9_12 import (
    EquipeLocalizacao, OrdemServico,
    LogTriagemIA, PrevisaoDemanda, RelatorioMensal,
)

__all__ = [
    "Usuario", "Secretaria", "Categoria", "Bairro", "Chamado", "Comentario",
    "VotoChamado", "PontosUsuario", "ConquistaUsuario",
    "SensorIoT", "LeituraSensor",
    "PropostaOrcamento", "VotoProposta",
    "RegistroAuditoria",
    "Fornecedor", "ContratoFornecedor",
    "SolicitacaoLGPD",
    "EquipeLocalizacao", "OrdemServico",
    "LogTriagemIA", "PrevisaoDemanda", "RelatorioMensal",
]
