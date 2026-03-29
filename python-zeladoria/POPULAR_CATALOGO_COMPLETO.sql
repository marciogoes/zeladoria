-- ========================================
-- POPULAR CATÁLOGO COMPLETO DE SERVIÇOS
-- 68 Serviços distribuídos em 12 Secretarias
-- ========================================

-- Criar tabela de serviços (se não existir)
CREATE TABLE IF NOT EXISTS catalogo_servicos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    subcategoria VARCHAR(100),
    secretaria_sigla VARCHAR(20) NOT NULL,
    secretaria_nome VARCHAR(200) NOT NULL,
    sla_horas INTEGER NOT NULL,
    prioridade VARCHAR(20) NOT NULL CHECK (prioridade IN ('emergencial', 'alta', 'media', 'baixa', 'agendavel')),
    status VARCHAR(20) DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Limpar dados existentes (cuidado em produção!)
TRUNCATE TABLE catalogo_servicos RESTART IDENTITY CASCADE;

-- ==================== SEURB - SECRETARIA DE URBANISMO ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SEURB-001', 'Reparo de Iluminação Pública', 'Manutenção, reparo ou substituição de postes e luminárias de iluminação pública', 'Iluminação Pública', 'Manutenção Corretiva', 'SEURB', 'Secretaria de Urbanismo', 48, 'alta'),
('SEURB-002', 'Instalação de Nova Iluminação', 'Solicitação de instalação de iluminação pública em logradouro sem cobertura', 'Iluminação Pública', 'Instalação', 'SEURB', 'Secretaria de Urbanismo', 720, 'agendavel'),
('SEURB-003', 'Tapa-buraco em Via Pública', 'Correção emergencial de buracos e afundamentos em vias públicas asfaltadas', 'Pavimentação', 'Emergencial', 'SEURB', 'Secretaria de Urbanismo', 24, 'emergencial'),
('SEURB-004', 'Recapeamento Asfáltico', 'Recuperação de pavimento asfáltico deteriorado em vias públicas', 'Pavimentação', 'Manutenção', 'SEURB', 'Secretaria de Urbanismo', 1440, 'media'),
('SEURB-005', 'Limpeza de Bueiro e Boca de Lobo', 'Desobstrução e limpeza de sistema de drenagem urbana', 'Drenagem', 'Manutenção', 'SEURB', 'Secretaria de Urbanismo', 72, 'alta'),
('SEURB-006', 'Reparo de Calçada', 'Conserto de calçadas públicas danificadas ou com obstáculos', 'Calçadas', 'Manutenção', 'SEURB', 'Secretaria de Urbanismo', 240, 'baixa'),
('SEURB-007', 'Remoção de Entulho em Via Pública', 'Retirada de entulho e material de construção descartado irregularmente', 'Limpeza Urbana', 'Remoção', 'SEURB', 'Secretaria de Urbanismo', 96, 'media'),
('SEURB-008', 'Poda de Árvore em Área Pública', 'Poda ou remoção de árvores que ofereçam risco ou obstrução', 'Arborização', 'Manutenção', 'SEURB', 'Secretaria de Urbanismo', 168, 'baixa'),
('SEURB-009', 'Plantio de Árvores', 'Solicitação de plantio de mudas em áreas públicas conforme plano diretor', 'Arborização', 'Plantio', 'SEURB', 'Secretaria de Urbanismo', 720, 'agendavel'),
('SEURB-010', 'Fiscalização de Obra Irregular', 'Denúncia de construção irregular ou sem autorização', 'Fiscalização', 'Denúncia', 'SEURB', 'Secretaria de Urbanismo', 120, 'media');

-- ==================== SESAN - SECRETARIA DE SANEAMENTO ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SESAN-001', 'Limpeza de Terreno Baldio', 'Limpeza e remoção de mato, lixo e entulho em terrenos abandonados', 'Limpeza Urbana', 'Terrenos', 'SESAN', 'Secretaria de Saneamento', 120, 'media'),
('SESAN-002', 'Coleta de Lixo Irregular', 'Recolhimento especial de lixo acumulado ou descartado irregularmente', 'Coleta de Resíduos', 'Coleta Especial', 'SESAN', 'Secretaria de Saneamento', 72, 'alta'),
('SESAN-003', 'Coleta de Entulho', 'Agendamento de coleta de entulho residencial (até 1m³)', 'Coleta de Resíduos', 'Entulho', 'SESAN', 'Secretaria de Saneamento', 168, 'agendavel'),
('SESAN-004', 'Coleta de Móveis Velhos', 'Recolhimento de móveis e objetos volumosos inutilizados', 'Coleta de Resíduos', 'Volumosos', 'SESAN', 'Secretaria de Saneamento', 168, 'agendavel'),
('SESAN-005', 'Dedetização de Imóvel Público', 'Controle de pragas e vetores em áreas públicas', 'Controle de Pragas', 'Dedetização', 'SESAN', 'Secretaria de Saneamento', 96, 'alta'),
('SESAN-006', 'Capina de Via Pública', 'Roçagem e limpeza de mato em canteiros e vias públicas', 'Limpeza Urbana', 'Capina', 'SESAN', 'Secretaria de Saneamento', 240, 'baixa'),
('SESAN-007', 'Limpeza de Canal e Igarapé', 'Desassoreamento e limpeza de canais de drenagem natural', 'Drenagem', 'Canais', 'SESAN', 'Secretaria de Saneamento', 336, 'media'),
('SESAN-008', 'Recolhimento de Animal Morto', 'Remoção de animal morto em via pública', 'Limpeza Urbana', 'Emergencial', 'SESAN', 'Secretaria de Saneamento', 24, 'emergencial');

-- ==================== SECON - SECRETARIA DE ECONOMIA ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SECON-001', 'Emissão de Alvará de Funcionamento', 'Solicitação de alvará para abertura de estabelecimento comercial', 'Licenciamento', 'Alvará', 'SECON', 'Secretaria de Economia', 240, 'agendavel'),
('SECON-002', 'Renovação de Alvará', 'Renovação anual de alvará de funcionamento', 'Licenciamento', 'Renovação', 'SECON', 'Secretaria de Economia', 168, 'media'),
('SECON-003', 'Fiscalização de Comércio Irregular', 'Denúncia de estabelecimento funcionando sem alvará ou licença', 'Fiscalização', 'Denúncia', 'SECON', 'Secretaria de Economia', 96, 'media'),
('SECON-004', 'Emissão de ISS', 'Cadastro e emissão de nota fiscal de serviço', 'Tributos', 'ISS', 'SECON', 'Secretaria de Economia', 72, 'media'),
('SECON-005', 'Emissão de Certidão Negativa', 'Emissão de certidão de débitos tributários', 'Certidões', 'Tributos', 'SECON', 'Secretaria de Economia', 48, 'media'),
('SECON-006', 'Parcelamento de IPTU', 'Solicitação de parcelamento de dívida de IPTU', 'Tributos', 'IPTU', 'SECON', 'Secretaria de Economia', 120, 'agendavel'),
('SECON-007', 'Autorização para Evento Comercial', 'Licença para realização de evento comercial em área pública', 'Licenciamento', 'Eventos', 'SECON', 'Secretaria de Economia', 336, 'agendavel');

-- ==================== SESMA - SECRETARIA DE SAÚDE ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SESMA-001', 'Agendamento de Consulta Básica', 'Agendamento de consulta médica em Unidade Básica de Saúde', 'Atendimento', 'Consulta', 'SESMA', 'Secretaria de Saúde', 168, 'media'),
('SESMA-002', 'Vacinação', 'Agendamento para vacinação conforme calendário nacional', 'Prevenção', 'Vacina', 'SESMA', 'Secretaria de Saúde', 48, 'alta'),
('SESMA-003', 'Controle de Zoonoses', 'Controle de animais sinantrópicos (morcegos, ratos, pombos)', 'Vigilância Sanitária', 'Zoonoses', 'SESMA', 'Secretaria de Saúde', 96, 'alta'),
('SESMA-004', 'Fiscalização Sanitária', 'Denúncia de irregularidade sanitária em estabelecimento', 'Vigilância Sanitária', 'Fiscalização', 'SESMA', 'Secretaria de Saúde', 72, 'alta'),
('SESMA-005', 'Emissão de Cartão SUS', 'Solicitação de Cartão Nacional de Saúde', 'Cadastro', 'Documentação', 'SESMA', 'Secretaria de Saúde', 96, 'media'),
('SESMA-006', 'Agendamento de Exame', 'Agendamento de exames laboratoriais e de imagem', 'Atendimento', 'Exames', 'SESMA', 'Secretaria de Saúde', 240, 'media'),
('SESMA-007', 'Remoção de Paciente', 'Solicitação de ambulância para transporte não emergencial', 'Transporte', 'Remoção', 'SESMA', 'Secretaria de Saúde', 48, 'alta');

-- ==================== SEMEC - SECRETARIA DE EDUCAÇÃO ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SEMEC-001', 'Matrícula Escolar', 'Solicitação de matrícula em escola municipal', 'Matrícula', 'Inicial', 'SEMEC', 'Secretaria de Educação', 240, 'agendavel'),
('SEMEC-002', 'Transferência Escolar', 'Solicitação de transferência entre escolas municipais', 'Matrícula', 'Transferência', 'SEMEC', 'Secretaria de Educação', 168, 'media'),
('SEMEC-003', 'Solicitação de Vaga em Creche', 'Cadastro para vaga em creche municipal', 'Matrícula', 'Educação Infantil', 'SEMEC', 'Secretaria de Educação', 720, 'agendavel'),
('SEMEC-004', 'Declaração de Escolaridade', 'Emissão de declaração de matrícula ou conclusão', 'Documentação', 'Declaração', 'SEMEC', 'Secretaria de Educação', 48, 'media'),
('SEMEC-005', 'Reparo em Escola', 'Solicitação de manutenção predial em escola municipal', 'Manutenção', 'Estrutura', 'SEMEC', 'Secretaria de Educação', 168, 'alta'),
('SEMEC-006', 'Solicitação de Merenda Escolar', 'Reclamação ou sugestão sobre merenda escolar', 'Alimentação', 'Merenda', 'SEMEC', 'Secretaria de Educação', 72, 'alta');

-- ==================== SEMAJ - SECRETARIA DE MEIO AMBIENTE ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SEMAJ-001', 'Denúncia de Crime Ambiental', 'Denúncia de desmatamento, poluição ou maus-tratos a animais', 'Fiscalização', 'Crime Ambiental', 'SEMAJ', 'Secretaria de Meio Ambiente', 48, 'emergencial'),
('SEMAJ-002', 'Autorização de Poda ou Corte', 'Solicitação de autorização para poda ou corte de árvore em propriedade privada', 'Licenciamento', 'Arborização', 'SEMAJ', 'Secretaria de Meio Ambiente', 240, 'agendavel'),
('SEMAJ-003', 'Coleta Seletiva', 'Informações e agendamento de coleta seletiva', 'Reciclagem', 'Coleta', 'SEMAJ', 'Secretaria de Meio Ambiente', 168, 'baixa'),
('SEMAJ-004', 'Licenciamento Ambiental', 'Solicitação de licença ambiental para atividades econômicas', 'Licenciamento', 'Ambiental', 'SEMAJ', 'Secretaria de Meio Ambiente', 720, 'agendavel'),
('SEMAJ-005', 'Resgate de Animal Silvestre', 'Solicitação de resgate de animal silvestre em área urbana', 'Fauna', 'Resgate', 'SEMAJ', 'Secretaria de Meio Ambiente', 24, 'emergencial');

-- ==================== SEMDEC - SECRETARIA DE DEFESA CIVIL ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SEMDEC-001', 'Emergência por Alagamento', 'Solicitação de socorro em caso de alagamento ou inundação', 'Emergência', 'Alagamento', 'SEMDEC', 'Secretaria de Defesa Civil', 2, 'emergencial'),
('SEMDEC-002', 'Risco de Desabamento', 'Denúncia de imóvel ou estrutura com risco de desabamento', 'Emergência', 'Estrutural', 'SEMDEC', 'Secretaria de Defesa Civil', 6, 'emergencial'),
('SEMDEC-003', 'Vistoria Preventiva', 'Solicitação de vistoria em imóvel com suspeita de risco', 'Prevenção', 'Vistoria', 'SEMDEC', 'Secretaria de Defesa Civil', 72, 'alta'),
('SEMDEC-004', 'Orientação sobre Risco', 'Orientação à população sobre áreas de risco', 'Prevenção', 'Orientação', 'SEMDEC', 'Secretaria de Defesa Civil', 168, 'baixa');

-- ==================== SEMDUH - SECRETARIA DE HABITAÇÃO ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SEMDUH-001', 'Cadastro Habitacional', 'Cadastro para programas de habitação popular', 'Habitação', 'Cadastro', 'SEMDUH', 'Secretaria de Habitação', 240, 'agendavel'),
('SEMDUH-002', 'Regularização Fundiária', 'Solicitação de regularização de imóvel', 'Regularização', 'Fundiária', 'SEMDUH', 'Secretaria de Habitação', 2160, 'agendavel'),
('SEMDUH-003', 'Melhorias Habitacionais', 'Solicitação de melhorias em moradia popular', 'Habitação', 'Melhoria', 'SEMDUH', 'Secretaria de Habitação', 720, 'media');

-- ==================== SETRA - SECRETARIA DE TRÂNSITO ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SETRA-001', 'Instalação de Semáforo', 'Solicitação de instalação de semáforo em cruzamento', 'Sinalização', 'Semáforo', 'SETRA', 'Secretaria de Trânsito', 720, 'agendavel'),
('SETRA-002', 'Reparo de Semáforo', 'Reparo de semáforo apagado ou com defeito', 'Sinalização', 'Manutenção', 'SETRA', 'Secretaria de Trânsito', 24, 'emergencial'),
('SETRA-003', 'Pintura de Faixa de Pedestre', 'Repintura ou instalação de faixa de pedestres', 'Sinalização', 'Horizontal', 'SETRA', 'Secretaria de Trânsito', 168, 'media'),
('SETRA-004', 'Instalação de Placa de Trânsito', 'Instalação de placa de sinalização viária', 'Sinalização', 'Vertical', 'SETRA', 'Secretaria de Trânsito', 240, 'baixa'),
('SETRA-005', 'Autorização de Evento em Via', 'Autorização para interdição de via para evento', 'Autorização', 'Eventos', 'SETRA', 'Secretaria de Trânsito', 336, 'agendavel'),
('SETRA-006', 'Lombada ou Quebra-molas', 'Solicitação de instalação de redutor de velocidade', 'Segurança Viária', 'Redutor', 'SETRA', 'Secretaria de Trânsito', 480, 'media');

-- ==================== FUNPAPA - ASSISTÊNCIA SOCIAL ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('FUNPAPA-001', 'Cadastro no Bolsa Família', 'Cadastro ou atualização no CadÚnico e Bolsa Família', 'Assistência', 'Cadastro', 'FUNPAPA', 'Fundação Papa João XXIII', 168, 'media'),
('FUNPAPA-002', 'Solicitação de Cesta Básica', 'Solicitação de cesta básica para famílias em vulnerabilidade', 'Assistência', 'Alimentação', 'FUNPAPA', 'Fundação Papa João XXIII', 96, 'alta'),
('FUNPAPA-003', 'Orientação Social', 'Atendimento com assistente social', 'Assistência', 'Orientação', 'FUNPAPA', 'Fundação Papa João XXIII', 120, 'media'),
('FUNPAPA-004', 'Denúncia de Violência', 'Denúncia de violência contra criança, idoso ou mulher', 'Proteção', 'Denúncia', 'FUNPAPA', 'Fundação Papa João XXIII', 24, 'emergencial'),
('FUNPAPA-005', 'Abrigamento Temporário', 'Solicitação de abrigo para pessoa em situação de rua', 'Assistência', 'Abrigamento', 'FUNPAPA', 'Fundação Papa João XXIII', 12, 'emergencial');

-- ==================== SECULT - SECRETARIA DE CULTURA ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SECULT-001', 'Autorização de Evento Cultural', 'Autorização para evento cultural em espaço público', 'Eventos', 'Autorização', 'SECULT', 'Secretaria de Cultura', 240, 'agendavel'),
('SECULT-002', 'Inscrição em Oficina Cultural', 'Inscrição em oficinas e cursos culturais gratuitos', 'Educação Cultural', 'Oficinas', 'SECULT', 'Secretaria de Cultura', 168, 'baixa'),
('SECULT-003', 'Uso de Espaço Cultural', 'Solicitação de uso de teatro, centro cultural ou biblioteca', 'Espaços', 'Agendamento', 'SECULT', 'Secretaria de Cultura', 336, 'agendavel'),
('SECULT-004', 'Registro de Patrimônio', 'Solicitação de registro de bem cultural ou patrimônio', 'Patrimônio', 'Registro', 'SECULT', 'Secretaria de Cultura', 720, 'baixa');

-- ==================== SETEL - SECRETARIA DE TELECOMUNICAÇÕES ====================
INSERT INTO catalogo_servicos (codigo, nome, descricao, categoria, subcategoria, secretaria_sigla, secretaria_nome, sla_horas, prioridade) VALUES
('SETEL-001', 'Instalação de Wi-Fi Público', 'Solicitação de ponto de internet gratuita em praça ou espaço público', 'Conectividade', 'Wi-Fi', 'SETEL', 'Secretaria de Telecomunicações', 720, 'baixa'),
('SETEL-002', 'Reparo de Wi-Fi Público', 'Manutenção de ponto de internet pública com defeito', 'Conectividade', 'Manutenção', 'SETEL', 'Secretaria de Telecomunicações', 96, 'media'),
('SETEL-003', 'Câmeras de Monitoramento', 'Solicitação de instalação de câmera de segurança', 'Segurança', 'Monitoramento', 'SETEL', 'Secretaria de Telecomunicações', 1440, 'agendavel');

-- Verificar total de serviços inseridos
SELECT 
    COUNT(*) as total_servicos,
    COUNT(DISTINCT secretaria_sigla) as total_secretarias
FROM catalogo_servicos;

-- Mostrar estatísticas por secretaria
SELECT 
    secretaria_sigla,
    secretaria_nome,
    COUNT(*) as total_servicos,
    COUNT(CASE WHEN prioridade = 'emergencial' THEN 1 END) as emergenciais
FROM catalogo_servicos
GROUP BY secretaria_sigla, secretaria_nome
ORDER BY total_servicos DESC;

-- Mostrar estatísticas por prioridade
SELECT 
    prioridade,
    COUNT(*) as total,
    ROUND(AVG(sla_horas), 2) as sla_medio_horas
FROM catalogo_servicos
GROUP BY prioridade
ORDER BY 
    CASE prioridade
        WHEN 'emergencial' THEN 1
        WHEN 'alta' THEN 2
        WHEN 'media' THEN 3
        WHEN 'baixa' THEN 4
        WHEN 'agendavel' THEN 5
    END;

-- ✅ SUCESSO! 68 SERVIÇOS CADASTRADOS!
