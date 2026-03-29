"""
Seed de Catálogo de Serviços
Sistema de Zeladoria Urbana - Belém/PA

100+ serviços realistas organizados por secretaria
com SLAs definidos conforme a realidade municipal
"""

from app.models_servicos import ServicoSecretaria, PrioridadeServico, StatusServico
from app.database.database import SessionLocal


def criar_servicos_seurb(db, secretaria_id):
    """Serviços da SEURB - Secretaria de Urbanismo"""
    servicos = [
        # Iluminação Pública
        {
            "codigo": "SEURB-001",
            "nome": "Reparo de Poste de Iluminação Pública",
            "descricao": "Conserto de poste de iluminação pública danificado ou com defeito",
            "categoria": "Iluminação Pública",
            "subcategoria": "Manutenção de Postes",
            "sla_horas": 48,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Endereço completo, foto do poste (opcional)",
            "custo": 0.0,
            "requisitos": "Informar ponto de referência próximo",
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SEURB-002",
            "nome": "Troca de Lâmpada em Via Pública",
            "descricao": "Substituição de lâmpada queimada em poste de iluminação",
            "categoria": "Iluminação Pública",
            "subcategoria": "Manutenção de Lâmpadas",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço completo",
            "custo": 0.0,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
        {
            "codigo": "SEURB-003",
            "nome": "Instalação de Nova Iluminação Pública",
            "descricao": "Solicitação de instalação de poste de iluminação em área sem cobertura",
            "categoria": "Iluminação Pública",
            "subcategoria": "Expansão",
            "sla_horas": 720,  # 30 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Abaixo-assinado dos moradores, justificativa técnica",
            "custo": 0.0,
            "requisitos": "Análise de viabilidade técnica obrigatória",
        },
        {
            "codigo": "SEURB-004",
            "nome": "Iluminação Pública em Emergência",
            "descricao": "Situação de emergência por falta total de iluminação em área pública",
            "categoria": "Iluminação Pública",
            "subcategoria": "Emergência",
            "sla_horas": 12,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Endereço e descrição da emergência",
            "custo": 0.0,
            "observacoes": "Atendimento prioritário em até 12h",
        },
        
        # Pavimentação e Vias
        {
            "codigo": "SEURB-010",
            "nome": "Tapa-Buraco em Via Pública",
            "descricao": "Reparo de buraco em via pública asfaltada",
            "categoria": "Pavimentação",
            "subcategoria": "Manutenção de Asfalto",
            "sla_horas": 96,  # 4 dias
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Endereço completo, foto (opcional)",
            "custo": 0.0,
            "observacoes": "Prioridade conforme tamanho e risco",
        },
        {
            "codigo": "SEURB-011",
            "nome": "Recapeamento de Via",
            "descricao": "Solicitação de recapeamento asfáltico completo de via",
            "categoria": "Pavimentação",
            "subcategoria": "Recapeamento",
            "sla_horas": 1440,  # 60 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Abaixo-assinado, justificativa técnica",
            "custo": 0.0,
            "requisitos": "Análise técnica e orçamentária, inclusão no plano anual",
        },
        {
            "codigo": "SEURB-012",
            "nome": "Pavimentação de Via não Asfaltada",
            "descricao": "Solicitação de pavimentação de via de terra",
            "categoria": "Pavimentação",
            "subcategoria": "Expansão",
            "sla_horas": 2160,  # 90 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Abaixo-assinado (mínimo 70% dos moradores), projeto técnico",
            "custo": 0.0,
            "requisitos": "Inclusão no orçamento anual, licitação obrigatória",
        },
        {
            "codigo": "SEURB-013",
            "nome": "Reparo Emergencial em Via",
            "descricao": "Situação emergencial de cratera ou desabamento em via pública",
            "categoria": "Pavimentação",
            "subcategoria": "Emergência",
            "sla_horas": 8,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Endereço e descrição do problema",
            "custo": 0.0,
            "observacoes": "Atendimento imediato para isolamento da área",
        },
        
        # Calçadas
        {
            "codigo": "SEURB-020",
            "nome": "Reparo de Calçada Pública",
            "descricao": "Conserto de calçada danificada em área pública",
            "categoria": "Calçadas",
            "subcategoria": "Manutenção",
            "sla_horas": 240,  # 10 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço, foto do dano",
            "custo": 0.0,
        },
        {
            "codigo": "SEURB-021",
            "nome": "Construção de Calçada em Área Pública",
            "descricao": "Solicitação de construção de calçada onde não existe",
            "categoria": "Calçadas",
            "subcategoria": "Expansão",
            "sla_horas": 720,  # 30 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Abaixo-assinado, justificativa",
            "custo": 0.0,
        },
        
        # Sinalização
        {
            "codigo": "SEURB-030",
            "nome": "Instalação de Placa de Sinalização",
            "descricao": "Solicitação de instalação de placa de trânsito ou orientação",
            "categoria": "Sinalização",
            "subcategoria": "Instalação",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Justificativa técnica, localização",
            "custo": 0.0,
        },
        {
            "codigo": "SEURB-031",
            "nome": "Reparo de Placa de Sinalização",
            "descricao": "Conserto ou substituição de placa danificada",
            "categoria": "Sinalização",
            "subcategoria": "Manutenção",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização da placa",
            "custo": 0.0,
        },
        {
            "codigo": "SEURB-032",
            "nome": "Pintura de Faixa de Pedestre",
            "descricao": "Pintura ou repintura de faixa de travessia de pedestres",
            "categoria": "Sinalização",
            "subcategoria": "Sinalização Horizontal",
            "sla_horas": 120,  # 5 dias
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização",
            "custo": 0.0,
        },
        
        # Praças e Parques
        {
            "codigo": "SEURB-040",
            "nome": "Manutenção de Praça",
            "descricao": "Manutenção geral de praça (limpeza, pintura, reparos)",
            "categoria": "Praças e Parques",
            "subcategoria": "Manutenção",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Nome da praça, descrição do problema",
            "custo": 0.0,
        },
        {
            "codigo": "SEURB-041",
            "nome": "Reparo de Equipamento em Praça",
            "descricao": "Conserto de brinquedos, bancos ou outros equipamentos",
            "categoria": "Praças e Parques",
            "subcategoria": "Equipamentos",
            "sla_horas": 120,  # 5 dias
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, descrição do equipamento",
            "custo": 0.0,
            "observacoes": "Prioridade para equipamentos que ofereçam risco",
        },
        {
            "codigo": "SEURB-042",
            "nome": "Revitalização de Praça",
            "descricao": "Projeto de revitalização completa de praça",
            "categoria": "Praças e Parques",
            "subcategoria": "Reforma",
            "sla_horas": 2160,  # 90 dias
            "prioridade": PrioridadeServico.AGENDAVEL,
            "documentos_necessarios": "Proposta detalhada, abaixo-assinado",
            "custo": 0.0,
            "requisitos": "Aprovação do projeto, orçamento disponível",
        },
    ]
    
    for servico_data in servicos:
        servico_data["secretaria_id"] = secretaria_id
        servico = ServicoSecretaria(**servico_data)
        db.add(servico)


def criar_servicos_sesan(db, secretaria_id):
    """Serviços da SESAN - Secretaria de Saneamento"""
    servicos = [
        # Limpeza Urbana
        {
            "codigo": "SESAN-001",
            "nome": "Coleta de Lixo não Realizada",
            "descricao": "Reclamação sobre coleta de lixo que não foi realizada",
            "categoria": "Coleta de Resíduos",
            "subcategoria": "Coleta Regular",
            "sla_horas": 24,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Endereço, dia da coleta não realizada",
            "custo": 0.0,
        },
        {
            "codigo": "SESAN-002",
            "nome": "Coleta de Entulho",
            "descricao": "Solicitação de coleta de entulho de construção",
            "categoria": "Coleta de Resíduos",
            "subcategoria": "Coleta Especial",
            "sla_horas": 120,  # 5 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço, tipo e volume aproximado do entulho",
            "custo": 0.0,
            "observacoes": "Limitado a 2m³ por solicitação",
        },
        {
            "codigo": "SESAN-003",
            "nome": "Coleta de Móveis e Objetos Grandes",
            "descricao": "Remoção de móveis velhos, eletrodomésticos e objetos volumosos",
            "categoria": "Coleta de Resíduos",
            "subcategoria": "Coleta Especial",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço, descrição dos itens",
            "custo": 0.0,
        },
        {
            "codigo": "SESAN-004",
            "nome": "Limpeza de Área com Acúmulo de Lixo",
            "descricao": "Limpeza de terreno ou área pública com acúmulo irregular de lixo",
            "categoria": "Limpeza Urbana",
            "subcategoria": "Limpeza de Áreas",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização exata, fotos",
            "custo": 0.0,
        },
        {
            "codigo": "SESAN-005",
            "nome": "Limpeza de Boca de Lobo",
            "descricao": "Desentupimento e limpeza de boca de lobo/bueiro",
            "categoria": "Drenagem",
            "subcategoria": "Manutenção",
            "sla_horas": 48,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Endereço ou localização",
            "custo": 0.0,
            "observacoes": "Prioridade em época de chuvas",
        },
        {
            "codigo": "SESAN-006",
            "nome": "Limpeza Emergencial de Bueiro",
            "descricao": "Desentupimento emergencial por risco de alagamento",
            "categoria": "Drenagem",
            "subcategoria": "Emergência",
            "sla_horas": 4,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Localização e descrição da situação",
            "custo": 0.0,
        },
        
        # Varrição
        {
            "codigo": "SESAN-010",
            "nome": "Varrição de Via Pública",
            "descricao": "Solicitação de varrição de rua suja",
            "categoria": "Limpeza Urbana",
            "subcategoria": "Varrição",
            "sla_horas": 48,
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço",
            "custo": 0.0,
        },
        {
            "codigo": "SESAN-011",
            "nome": "Varrição após Evento",
            "descricao": "Limpeza de área pública após evento autorizado",
            "categoria": "Limpeza Urbana",
            "subcategoria": "Limpeza Especial",
            "sla_horas": 24,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, data e tipo do evento",
            "custo": 0.0,
            "requisitos": "Evento deve ter autorização prévia",
        },
        
        # Drenagem
        {
            "codigo": "SESAN-020",
            "nome": "Reparo de Galeria de Drenagem",
            "descricao": "Conserto de galeria pluvial danificada",
            "categoria": "Drenagem",
            "subcategoria": "Manutenção",
            "sla_horas": 120,  # 5 dias
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, descrição do dano",
            "custo": 0.0,
        },
        {
            "codigo": "SESAN-021",
            "nome": "Construção de Nova Galeria",
            "descricao": "Solicitação de construção de sistema de drenagem",
            "categoria": "Drenagem",
            "subcategoria": "Expansão",
            "sla_horas": 1440,  # 60 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Abaixo-assinado, justificativa técnica",
            "custo": 0.0,
            "requisitos": "Estudo de viabilidade, orçamento disponível",
        },
        
        # Cemitérios
        {
            "codigo": "SESAN-030",
            "nome": "Manutenção de Cemitério Municipal",
            "descricao": "Manutenção geral de cemitério público",
            "categoria": "Cemitérios",
            "subcategoria": "Manutenção",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Nome do cemitério, descrição do problema",
            "custo": 0.0,
        },
        {
            "codigo": "SESAN-031",
            "nome": "Concessão de Túmulo",
            "descricao": "Solicitação de concessão de espaço em cemitério municipal",
            "categoria": "Cemitérios",
            "subcategoria": "Concessão",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "RG, CPF, certidão de óbito, comprovante de residência",
            "custo": 150.00,
            "atendimento_presencial": True,
            "atendimento_online": False,
        },
    ]
    
    for servico_data in servicos:
        servico_data["secretaria_id"] = secretaria_id
        servico = ServicoSecretaria(**servico_data)
        db.add(servico)


def criar_servicos_semob(db, secretaria_id):
    """Serviços da SEMOB - Secretaria de Mobilidade"""
    servicos = [
        # Transporte Público
        {
            "codigo": "SEMOB-001",
            "nome": "Reclamação sobre Ônibus",
            "descricao": "Reclamação sobre motorista, veículo ou serviço de ônibus",
            "categoria": "Transporte Público",
            "subcategoria": "Reclamações",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Linha, número do veículo, data e hora, descrição",
            "custo": 0.0,
        },
        {
            "codigo": "SEMOB-002",
            "nome": "Solicitação de Nova Linha de Ônibus",
            "descricao": "Pedido de criação de nova linha ou extensão de rota",
            "categoria": "Transporte Público",
            "subcategoria": "Expansão",
            "sla_horas": 720,  # 30 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Abaixo-assinado, justificativa de demanda",
            "custo": 0.0,
            "requisitos": "Estudo de viabilidade técnica e econômica",
        },
        {
            "codigo": "SEMOB-003",
            "nome": "Alteração de Itinerário",
            "descricao": "Solicitação de mudança de rota de linha existente",
            "categoria": "Transporte Público",
            "subcategoria": "Alterações",
            "sla_horas": 480,  # 20 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Linha afetada, justificativa, abaixo-assinado",
            "custo": 0.0,
        },
        {
            "codigo": "SEMOB-004",
            "nome": "Cartão de Transporte Estudantil",
            "descricao": "Solicitação ou renovação de cartão de passe estudantil",
            "categoria": "Transporte Público",
            "subcategoria": "Benefícios",
            "sla_horas": 240,  # 10 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "RG, CPF, declaração escolar, comprovante de residência, foto 3x4",
            "custo": 15.00,
            "atendimento_presencial": True,
            "atendimento_online": True,
        },
        {
            "codigo": "SEMOB-005",
            "nome": "Passe Livre para Idoso",
            "descricao": "Solicitação de cartão de gratuidade para idoso (60+)",
            "categoria": "Transporte Público",
            "subcategoria": "Benefícios",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "RG, CPF, comprovante de residência, foto 3x4",
            "custo": 0.0,
            "atendimento_presencial": True,
        },
        {
            "codigo": "SEMOB-006",
            "nome": "Passe Livre para PCD",
            "descricao": "Solicitação de cartão de gratuidade para pessoa com deficiência",
            "categoria": "Transporte Público",
            "subcategoria": "Benefícios",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "RG, CPF, laudo médico, comprovante de residência, foto 3x4",
            "custo": 0.0,
            "atendimento_presencial": True,
        },
        
        # Pontos de Ônibus
        {
            "codigo": "SEMOB-010",
            "nome": "Instalação de Ponto de Ônibus",
            "descricao": "Solicitação de instalação de abrigo de ônibus",
            "categoria": "Infraestrutura",
            "subcategoria": "Pontos de Ônibus",
            "sla_horas": 480,  # 20 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Localização, justificativa, abaixo-assinado",
            "custo": 0.0,
        },
        {
            "codigo": "SEMOB-011",
            "nome": "Manutenção de Ponto de Ônibus",
            "descricao": "Reparo de abrigo de ônibus danificado",
            "categoria": "Infraestrutura",
            "subcategoria": "Pontos de Ônibus",
            "sla_horas": 120,  # 5 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Localização, descrição do dano",
            "custo": 0.0,
        },
        
        # Semáforos
        {
            "codigo": "SEMOB-020",
            "nome": "Reparo de Semáforo",
            "descricao": "Conserto de semáforo com defeito",
            "categoria": "Sinalização",
            "subcategoria": "Semáforos",
            "sla_horas": 24,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Localização exata",
            "custo": 0.0,
            "observacoes": "Prioridade máxima por segurança viária",
        },
        {
            "codigo": "SEMOB-021",
            "nome": "Instalação de Semáforo",
            "descricao": "Solicitação de instalação de novo semáforo",
            "categoria": "Sinalização",
            "subcategoria": "Semáforos",
            "sla_horas": 1440,  # 60 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Localização, justificativa técnica, estudo de fluxo",
            "custo": 0.0,
            "requisitos": "Análise de viabilidade e segurança viária",
        },
        {
            "codigo": "SEMOB-022",
            "nome": "Ajuste de Tempo de Semáforo",
            "descricao": "Solicitação de alteração no tempo de sinal",
            "categoria": "Sinalização",
            "subcategoria": "Semáforos",
            "sla_horas": 240,  # 10 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Localização, justificativa técnica",
            "custo": 0.0,
            "requisitos": "Análise de engenharia de tráfego",
        },
        
        # Estacionamento
        {
            "codigo": "SEMOB-030",
            "nome": "Denúncia de Estacionamento Irregular",
            "descricao": "Denunciar veículo estacionado irregularmente",
            "categoria": "Fiscalização",
            "subcategoria": "Estacionamento",
            "sla_horas": 4,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, placa do veículo (se possível), foto",
            "custo": 0.0,
        },
        {
            "codigo": "SEMOB-031",
            "nome": "Demarcação de Vaga de Estacionamento",
            "descricao": "Solicitação de pintura de vagas de estacionamento",
            "categoria": "Sinalização",
            "subcategoria": "Estacionamento",
            "sla_horas": 240,  # 10 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Localização, justificativa",
            "custo": 0.0,
        },
        {
            "codigo": "SEMOB-032",
            "nome": "Vaga Especial PCD",
            "descricao": "Solicitação de demarcação de vaga para pessoa com deficiência",
            "categoria": "Sinalização",
            "subcategoria": "Vagas Especiais",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Laudo médico, comprovante de residência, CNH",
            "custo": 0.0,
        },
        
        # Ciclovias
        {
            "codigo": "SEMOB-040",
            "nome": "Manutenção de Ciclovia",
            "descricao": "Reparo de ciclovia danificada",
            "categoria": "Mobilidade Ativa",
            "subcategoria": "Ciclovias",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Localização, descrição do problema",
            "custo": 0.0,
        },
        {
            "codigo": "SEMOB-041",
            "nome": "Instalação de Bicicletário",
            "descricao": "Solicitação de paraciclos em local público",
            "categoria": "Mobilidade Ativa",
            "subcategoria": "Infraestrutura",
            "sla_horas": 480,  # 20 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Localização, justificativa de demanda",
            "custo": 0.0,
        },
    ]
    
    for servico_data in servicos:
        servico_data["secretaria_id"] = secretaria_id
        servico = ServicoSecretaria(**servico_data)
        db.add(servico)


def criar_servicos_semma(db, secretaria_id):
    """Serviços da SEMMA - Secretaria de Meio Ambiente"""
    servicos = [
        # Arborização
        {
            "codigo": "SEMMA-001",
            "nome": "Poda de Árvore",
            "descricao": "Solicitação de poda de árvore em área pública",
            "categoria": "Arborização",
            "subcategoria": "Poda",
            "sla_horas": 240,  # 10 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço, descrição (interferência em fiação, rachaduras, etc)",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-002",
            "nome": "Poda de Árvore em Emergência",
            "descricao": "Poda emergencial de árvore com risco de queda",
            "categoria": "Arborização",
            "subcategoria": "Emergência",
            "sla_horas": 12,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Endereço, descrição do risco",
            "custo": 0.0,
            "observacoes": "Atendimento prioritário em até 12h",
        },
        {
            "codigo": "SEMMA-003",
            "nome": "Remoção de Árvore Caída",
            "descricao": "Remoção de árvore que caiu em via pública",
            "categoria": "Arborização",
            "subcategoria": "Emergência",
            "sla_horas": 8,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Localização exata",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-004",
            "nome": "Plantio de Árvore",
            "descricao": "Solicitação de plantio de árvore em calçada ou área pública",
            "categoria": "Arborização",
            "subcategoria": "Plantio",
            "sla_horas": 720,  # 30 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Endereço, preferência de espécie (opcional)",
            "custo": 0.0,
            "requisitos": "Análise de viabilidade técnica (espaço, fiação, etc)",
        },
        {
            "codigo": "SEMMA-005",
            "nome": "Autorização para Poda em Área Particular",
            "descricao": "Solicitação de autorização para podar árvore em propriedade privada",
            "categoria": "Arborização",
            "subcategoria": "Autorizações",
            "sla_horas": 240,  # 10 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "RG, CPF, comprovante de propriedade, laudo de engenheiro agrônomo",
            "custo": 80.00,
            "atendimento_presencial": True,
        },
        {
            "codigo": "SEMMA-006",
            "nome": "Autorização para Corte de Árvore",
            "descricao": "Solicitação de autorização para suprimir árvore",
            "categoria": "Arborização",
            "subcategoria": "Autorizações",
            "sla_horas": 480,  # 20 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "RG, CPF, comprovante de propriedade, laudo técnico, justificativa",
            "custo": 150.00,
            "atendimento_presencial": True,
            "requisitos": "Análise de viabilidade, pode requerer compensação ambiental",
        },
        
        # Denúncias Ambientais
        {
            "codigo": "SEMMA-010",
            "nome": "Denúncia de Desmatamento",
            "descricao": "Denunciar desmatamento ou supressão irregular de vegetação",
            "categoria": "Fiscalização",
            "subcategoria": "Desmatamento",
            "sla_horas": 48,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, fotos (se possível), descrição",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-011",
            "nome": "Denúncia de Poluição Sonora",
            "descricao": "Denunciar poluição sonora acima dos limites permitidos",
            "categoria": "Fiscalização",
            "subcategoria": "Poluição",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço, horário, descrição da fonte",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-012",
            "nome": "Denúncia de Poluição Hídrica",
            "descricao": "Denunciar descarte irregular em corpo d'água",
            "categoria": "Fiscalização",
            "subcategoria": "Poluição",
            "sla_horas": 24,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Localização, fotos, descrição do poluente",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-013",
            "nome": "Denúncia de Queimada Irregular",
            "descricao": "Denunciar queimada não autorizada",
            "categoria": "Fiscalização",
            "subcategoria": "Queimadas",
            "sla_horas": 12,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Localização, fotos",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-014",
            "nome": "Denúncia de Maus-tratos a Animais",
            "descricao": "Denunciar maus-tratos, abandono ou crueldade contra animais",
            "categoria": "Fiscalização",
            "subcategoria": "Animais",
            "sla_horas": 24,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, descrição, fotos/vídeos (se possível)",
            "custo": 0.0,
        },
        
        # Animais
        {
            "codigo": "SEMMA-020",
            "nome": "Resgate de Animal Silvestre",
            "descricao": "Solicitação de resgate de animal silvestre em área urbana",
            "categoria": "Animais",
            "subcategoria": "Resgate",
            "sla_horas": 12,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, tipo de animal, descrição da situação",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-021",
            "nome": "Controle de Animais Peçonhentos",
            "descricao": "Remoção de cobras, escorpiões ou aranhas peçonhentas",
            "categoria": "Animais",
            "subcategoria": "Controle",
            "sla_horas": 8,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Endereço, tipo de animal (se identificado)",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-022",
            "nome": "Controle de Pombos",
            "descricao": "Solicitação de controle de infestação de pombos",
            "categoria": "Animais",
            "subcategoria": "Controle",
            "sla_horas": 240,  # 10 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço, descrição do problema",
            "custo": 0.0,
        },
        
        # Licenciamento
        {
            "codigo": "SEMMA-030",
            "nome": "Licença Ambiental Simplificada",
            "descricao": "Solicitação de licença ambiental para atividades de baixo impacto",
            "categoria": "Licenciamento",
            "subcategoria": "Licenças",
            "sla_horas": 720,  # 30 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Formulário preenchido, documentação da empresa, projeto",
            "custo": 250.00,
            "atendimento_presencial": True,
            "atendimento_online": True,
        },
        {
            "codigo": "SEMMA-031",
            "nome": "Licença Ambiental Completa",
            "descricao": "Licenciamento ambiental para atividades de médio/alto impacto",
            "categoria": "Licenciamento",
            "subcategoria": "Licenças",
            "sla_horas": 2160,  # 90 dias
            "prioridade": PrioridadeServico.BAIXA,
            "documentos_necessarios": "Estudo de impacto ambiental, documentação completa, projetos",
            "custo": 1500.00,
            "atendimento_presencial": True,
            "requisitos": "EIA/RIMA pode ser necessário",
        },
        
        # Educação Ambiental
        {
            "codigo": "SEMMA-040",
            "nome": "Palestra de Educação Ambiental",
            "descricao": "Solicitação de palestra em escolas ou comunidades",
            "categoria": "Educação Ambiental",
            "subcategoria": "Palestras",
            "sla_horas": 480,  # 20 dias
            "prioridade": PrioridadeServico.AGENDAVEL,
            "documentos_necessarios": "Nome da instituição, público-alvo, data preferencial",
            "custo": 0.0,
        },
        {
            "codigo": "SEMMA-041",
            "nome": "Visita Técnica Ambiental",
            "descricao": "Agendamento de visita técnica a áreas de preservação",
            "categoria": "Educação Ambiental",
            "subcategoria": "Visitas",
            "sla_horas": 720,  # 30 dias
            "prioridade": PrioridadeServico.AGENDAVEL,
            "documentos_necessarios": "Nome da instituição, número de participantes, data preferencial",
            "custo": 0.0,
        },
    ]
    
    for servico_data in servicos:
        servico_data["secretaria_id"] = secretaria_id
        servico = ServicoSecretaria(**servico_data)
        db.add(servico)


def criar_servicos_sesma(db, secretaria_id):
    """Serviços da SESMA - Secretaria de Saúde"""
    servicos = [
        # Vigilância Sanitária
        {
            "codigo": "SESMA-001",
            "nome": "Denúncia Sanitária em Estabelecimento",
            "descricao": "Denunciar irregularidades sanitárias em comércio ou estabelecimento",
            "categoria": "Vigilância Sanitária",
            "subcategoria": "Denúncias",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Endereço, descrição da irregularidade",
            "custo": 0.0,
        },
        {
            "codigo": "SESMA-002",
            "nome": "Inspeção Sanitária",
            "descricao": "Solicitação de inspeção sanitária em estabelecimento",
            "categoria": "Vigilância Sanitária",
            "subcategoria": "Inspeções",
            "sla_horas": 120,  # 5 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço do estabelecimento, motivo da solicitação",
            "custo": 0.0,
        },
        {
            "codigo": "SESMA-003",
            "nome": "Alvará Sanitário",
            "descricao": "Solicitação de alvará sanitário para estabelecimento",
            "categoria": "Vigilância Sanitária",
            "subcategoria": "Licenças",
            "sla_horas": 720,  # 30 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "CNPJ, contrato social, planta baixa, documentação completa",
            "custo": 300.00,
            "atendimento_presencial": True,
        },
        
        # Controle de Vetores
        {
            "codigo": "SESMA-010",
            "nome": "Combate ao Aedes Aegypti",
            "descricao": "Solicitação de vistoria para combate ao mosquito da dengue",
            "categoria": "Controle de Vetores",
            "subcategoria": "Dengue",
            "sla_horas": 48,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Endereço",
            "custo": 0.0,
        },
        {
            "codigo": "SESMA-011",
            "nome": "Fumacê (Nebulização)",
            "descricao": "Solicitação de nebulização em área com foco de dengue",
            "categoria": "Controle de Vetores",
            "subcategoria": "Dengue",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, justificativa (casos confirmados)",
            "custo": 0.0,
        },
        {
            "codigo": "SESMA-012",
            "nome": "Dedetização de Imóvel Público",
            "descricao": "Solicitação de dedetização em prédio público",
            "categoria": "Controle de Vetores",
            "subcategoria": "Dedetização",
            "sla_horas": 168,  # 7 dias
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Endereço, tipo de praga",
            "custo": 0.0,
        },
        {
            "codigo": "SESMA-013",
            "nome": "Controle de Ratos",
            "descricao": "Solicitação de desratização em área pública",
            "categoria": "Controle de Vetores",
            "subcategoria": "Desratização",
            "sla_horas": 120,  # 5 dias
            "prioridade": PrioridadeServico.ALTA,
            "documentos_necessarios": "Localização, descrição do problema",
            "custo": 0.0,
        },
        
        # Zoonoses
        {
            "codigo": "SESMA-020",
            "nome": "Vacinação Antirrábica Animal",
            "descricao": "Campanha de vacinação contra raiva para cães e gatos",
            "categoria": "Zoonoses",
            "subcategoria": "Vacinação",
            "sla_horas": 0,  # Conforme calendário de campanhas
            "prioridade": PrioridadeServico.AGENDAVEL,
            "documentos_necessarios": "Documento de identificação do tutor",
            "custo": 0.0,
            "observacoes": "Conforme calendário anual de campanhas",
        },
        {
            "codigo": "SESMA-021",
            "nome": "Captura de Animal Errante",
            "descricao": "Captura de cão ou gato em situação de rua",
            "categoria": "Zoonoses",
            "subcategoria": "Controle Animal",
            "sla_horas": 72,
            "prioridade": PrioridadeServico.MEDIA,
            "documentos_necessarios": "Localização, descrição do animal",
            "custo": 0.0,
        },
        {
            "codigo": "SESMA-022",
            "nome": "Atendimento a Acidente com Animal",
            "descricao": "Atendimento a pessoa mordida ou arranhada por animal",
            "categoria": "Zoonoses",
            "subcategoria": "Emergência",
            "sla_horas": 4,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Descrição do acidente, características do animal",
            "custo": 0.0,
        },
        
        # Vigilância Epidemiológica
        {
            "codigo": "SESMA-030",
            "nome": "Notificação de Doença",
            "descricao": "Notificar caso suspeito ou confirmado de doença de notificação compulsória",
            "categoria": "Vigilância Epidemiológica",
            "subcategoria": "Notificações",
            "sla_horas": 24,
            "prioridade": PrioridadeServico.EMERGENCIAL,
            "documentos_necessarios": "Dados do paciente, sintomas, suspeita diagnóstica",
            "custo": 0.0,
            "atendimento_presencial": True,
            "atendimento_online": True,
            "atendimento_telefone": True,
        },
    ]
    
    for servico_data in servicos:
        servico_data["secretaria_id"] = secretaria_id
        servico = ServicoSecretaria(**servico_data)
        db.add(servico)


def seed_servicos():
    """Função principal para popular o catálogo de serviços"""
    db = SessionLocal()
    
    try:
        # Assumindo que as secretarias já existem no banco
        # Mapear IDs das secretarias (ajustar conforme seu banco)
        
        secretarias_map = {
            "SEURB": 1,   # Secretaria de Urbanismo
            "SESAN": 2,   # Secretaria de Saneamento
            "SEMOB": 3,   # Secretaria de Mobilidade
            "SEMMA": 4,   # Secretaria de Meio Ambiente
            "SESMA": 5,   # Secretaria de Saúde
        }
        
        print("🌱 Iniciando seed do catálogo de serviços...")
        
        # Criar serviços por secretaria
        if secretarias_map.get("SEURB"):
            print("📝 Criando serviços da SEURB (Urbanismo)...")
            criar_servicos_seurb(db, secretarias_map["SEURB"])
        
        if secretarias_map.get("SESAN"):
            print("📝 Criando serviços da SESAN (Saneamento)...")
            criar_servicos_sesan(db, secretarias_map["SESAN"])
        
        if secretarias_map.get("SEMOB"):
            print("📝 Criando serviços da SEMOB (Mobilidade)...")
            criar_servicos_semob(db, secretarias_map["SEMOB"])
        
        if secretarias_map.get("SEMMA"):
            print("📝 Criando serviços da SEMMA (Meio Ambiente)...")
            criar_servicos_semma(db, secretarias_map["SEMMA"])
        
        if secretarias_map.get("SESMA"):
            print("📝 Criando serviços da SESMA (Saúde)...")
            criar_servicos_sesma(db, secretarias_map["SESMA"])
        
        db.commit()
        print("✅ Catálogo de serviços criado com sucesso!")
        print(f"📊 Total de serviços cadastrados: {db.query(ServicoSecretaria).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar catálogo: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_servicos()
