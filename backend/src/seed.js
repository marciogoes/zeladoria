const { sequelize, syncDatabase } = require('../src/config/database');
const { Usuario, Categoria, Bairro, Chamado } = require('../src/models');
const logger = require('../src/utils/logger');

const seed = async () => {
    try {
        logger.info('🌱 Iniciando seed do banco de dados...');

        // Sincronizar banco (criar tabelas)
        await syncDatabase(true); // force: true = apagar e recriar

        // Criar categorias
        logger.info('📦 Criando categorias...');
        const categorias = await Categoria.bulkCreate([
            { nome: 'Iluminação Pública', descricao: 'Problemas com postes e lâmpadas', icone: '💡', cor: '#FFA500', sla_horas: 24 },
            { nome: 'Buracos na Via', descricao: 'Buracos em ruas e avenidas', icone: '🕳️', cor: '#8B4513', sla_horas: 48 },
            { nome: 'Lixo e Limpeza', descricao: 'Lixo acumulado e falta de limpeza', icone: '🗑️', cor: '#228B22', sla_horas: 12 },
            { nome: 'Calçadas', descricao: 'Calçadas quebradas ou irregulares', icone: '🚶', cor: '#808080', sla_horas: 72 },
            { nome: 'Arborização', descricao: 'Poda e cuidados com árvores', icone: '🌳', cor: '#2E8B57', sla_horas: 48 },
            { nome: 'Sinalização', descricao: 'Placas e semáforos', icone: '🚦', cor: '#FF0000', sla_horas: 24 },
            { nome: 'Esgoto', descricao: 'Problemas com esgoto e drenagem', icone: '🚰', cor: '#4169E1', sla_horas: 12 },
            { nome: 'Pichação', descricao: 'Vandalismo e pichações', icone: '🎨', cor: '#DC143C', sla_horas: 168 }
        ]);
        logger.info(`✓ ${categorias.length} categorias criadas`);

        // Criar bairros de Belém
        logger.info('🏘️  Criando bairros...');
        const bairros = await Bairro.bulkCreate([
            { nome: 'Batista Campos', regiao: 'Centro' },
            { nome: 'Nazaré', regiao: 'Centro' },
            { nome: 'Umarizal', regiao: 'Centro' },
            { nome: 'Reduto', regiao: 'Centro' },
            { nome: 'Marco', regiao: 'Norte' },
            { nome: 'Pedreira', regiao: 'Norte' },
            { nome: 'Marambaia', regiao: 'Sul' },
            { nome: 'Cremação', regiao: 'Leste' },
            { nome: 'Guamá', regiao: 'Leste' },
            { nome: 'Telégrafo', regiao: 'Sul' }
        ]);
        logger.info(`✓ ${bairros.length} bairros criados`);

        // Criar usuários de teste
        logger.info('👤 Criando usuários...');
        const usuarios = await Usuario.bulkCreate([
            {
                nome: 'Pedro Almeida',
                email: 'pedro.almeida@email.com',
                senha: 'senha123',
                telefone: '(91) 98765-4321',
                cpf: '123.456.789-01',
                tipo: 'cidadao'
            },
            {
                nome: 'João Silva',
                email: 'joao.silva@belem.pa.gov.br',
                senha: 'senha123',
                telefone: '(91) 3242-1100',
                tipo: 'equipe'
            },
            {
                nome: 'Maria Santos',
                email: 'maria.santos@belem.pa.gov.br',
                senha: 'senha123',
                telefone: '(91) 3242-1101',
                tipo: 'gestor'
            },
            {
                nome: 'Admin Sistema',
                email: 'admin@belem.pa.gov.br',
                senha: 'senha123',
                telefone: '(91) 3242-1000',
                tipo: 'admin'
            }
        ]);
        logger.info(`✓ ${usuarios.length} usuários criados`);

        // Criar chamados de exemplo
        logger.info('📞 Criando chamados de exemplo...');
        const chamados = await Chamado.bulkCreate([
            {
                titulo: 'Lâmpada queimada na Av. Presidente Vargas',
                descricao: 'Poste 123 com lâmpada apagada há 3 dias',
                endereco: 'Av. Presidente Vargas, 456',
                latitude: -1.4558,
                longitude: -48.4902,
                usuario_id: 1,
                categoria_id: 1,
                bairro_id: 1,
                status: 'aberto',
                prioridade: 'alta'
            },
            {
                titulo: 'Buraco grande na Rua dos Mundurucus',
                descricao: 'Buraco com aproximadamente 1m de diâmetro causando risco',
                endereco: 'Rua dos Mundurucus, 789',
                latitude: -1.4500,
                longitude: -48.4850,
                usuario_id: 1,
                categoria_id: 2,
                bairro_id: 2,
                status: 'em_andamento',
                prioridade: 'critica',
                responsavel_id: 2
            },
            {
                titulo: 'Lixo acumulado na praça',
                descricao: 'Lixo não foi recolhido há 2 dias',
                endereco: 'Praça da República',
                latitude: -1.4520,
                longitude: -48.4920,
                usuario_id: 1,
                categoria_id: 3,
                bairro_id: 3,
                status: 'resolvido',
                prioridade: 'media',
                responsavel_id: 2,
                data_resolucao: new Date(),
                avaliacao: 5,
                comentario_avaliacao: 'Resolvido rapidamente, obrigado!'
            }
        ]);
        logger.info(`✓ ${chamados.length} chamados criados`);

        logger.info('✅ Seed concluído com sucesso!');
        logger.info('');
        logger.info('👤 Usuários criados:');
        logger.info('   Cidadão: pedro.almeida@email.com / senha123');
        logger.info('   Equipe: joao.silva@belem.pa.gov.br / senha123');
        logger.info('   Gestor: maria.santos@belem.pa.gov.br / senha123');
        logger.info('   Admin: admin@belem.pa.gov.br / senha123');

        process.exit(0);
    } catch (error) {
        logger.error('❌ Erro ao executar seed:', error);
        process.exit(1);
    }
};

seed();
