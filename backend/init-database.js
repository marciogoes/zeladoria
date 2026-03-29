/**
 * Script para inicializar o banco de dados SQLite
 * Cria tabelas e popula com dados iniciais de Belém/PA
 */

const { sequelize } = require('./src/config/database');
const bcrypt = require('bcryptjs');

async function initDatabase() {
  try {
    console.log('🔄 Iniciando banco de dados SQLite...\n');

    // Conectar ao banco
    await sequelize.authenticate();
    console.log('✓ Conectado ao SQLite');

    // Criar tabelas
    console.log('\n📋 Criando tabelas...');

    // Tabela de usuários
    await sequelize.query(`
      CREATE TABLE IF NOT EXISTS usuarios (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        cpf TEXT UNIQUE,
        telefone TEXT,
        tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('cidadao', 'campo', 'gestor', 'admin')),
        avatar_url TEXT,
        ativo INTEGER DEFAULT 1,
        email_verificado INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✓ Tabela usuarios criada');

    // Tabela de categorias
    await sequelize.query(`
      CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT,
        icone TEXT,
        cor TEXT,
        prioridade_padrao TEXT DEFAULT 'media',
        sla_horas INTEGER DEFAULT 168,
        ativo INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✓ Tabela categorias criada');

    // Tabela de bairros
    await sequelize.query(`
      CREATE TABLE IF NOT EXISTS bairros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        distrito TEXT,
        populacao INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✓ Tabela bairros criada');

    // Tabela de chamados
    await sequelize.query(`
      CREATE TABLE IF NOT EXISTS chamados (
        id TEXT PRIMARY KEY,
        protocolo TEXT UNIQUE NOT NULL,
        categoria_id INTEGER,
        cidadao_id TEXT,
        bairro_id INTEGER,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        endereco TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        status TEXT DEFAULT 'aberto' CHECK (status IN ('aberto', 'triagem', 'em_andamento', 'aguardando', 'concluido', 'cancelado')),
        prioridade TEXT DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta', 'critica')),
        data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_conclusao DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
        FOREIGN KEY (cidadao_id) REFERENCES usuarios(id),
        FOREIGN KEY (bairro_id) REFERENCES bairros(id)
      )
    `);
    console.log('✓ Tabela chamados criada');

    // Popular com dados iniciais
    console.log('\n📦 Populando dados iniciais...');

    // Verificar se já tem dados
    const [usuarios] = await sequelize.query('SELECT COUNT(*) as count FROM usuarios');
    
    if (usuarios[0].count === 0) {
      // Criar usuários de teste
      const senhaHash = await bcrypt.hash('senha123', 10);
      
      await sequelize.query(`
        INSERT INTO usuarios (id, nome, email, senha_hash, tipo_usuario)
        VALUES 
          ('user-admin', 'Administrador', 'admin@belem.pa.gov.br', '${senhaHash}', 'admin'),
          ('user-gestor', 'Gestor Municipal', 'gestor@belem.pa.gov.br', '${senhaHash}', 'gestor'),
          ('user-campo1', 'João Silva', 'joao.silva@belem.pa.gov.br', '${senhaHash}', 'campo'),
          ('user-cidadao1', 'Pedro Almeida', 'pedro.almeida@email.com', '${senhaHash}', 'cidadao'),
          ('user-cidadao2', 'Maria Santos', 'maria.santos@email.com', '${senhaHash}', 'cidadao')
      `);
      console.log('✓ Usuários criados');

      // Criar categorias
      await sequelize.query(`
        INSERT INTO categorias (nome, descricao, icone, cor, prioridade_padrao, sla_horas)
        VALUES 
          ('Iluminação Pública', 'Problemas com postes e lâmpadas', 'lightbulb', '#F59E0B', 'alta', 48),
          ('Buraco na Via', 'Buracos e problemas no asfalto', 'wrench', '#EF4444', 'critica', 24),
          ('Lixo Acumulado', 'Acúmulo de lixo em vias públicas', 'trash-2', '#10B981', 'media', 24),
          ('Poda de Árvore', 'Árvores com galhos sobre fiação', 'tree-pine', '#22C55E', 'alta', 72),
          ('Sinalização', 'Placas e semáforos', 'navigation', '#3B82F6', 'critica', 12),
          ('Calçada Irregular', 'Calçadas quebradas', 'hard-hat', '#8B5CF6', 'media', 168)
      `);
      console.log('✓ Categorias criadas');

      // Criar bairros de Belém
      await sequelize.query(`
        INSERT INTO bairros (nome, distrito, populacao)
        VALUES 
          ('Campina', 'DABEL', 15000),
          ('Cidade Velha', 'DABEL', 18000),
          ('Umarizal', 'DABEL', 14000),
          ('Nazaré', 'DABEL', 10000),
          ('Marco', 'DABEL', 25000),
          ('Batista Campos', 'DABEL', 12000),
          ('Pedreira', 'DABEL', 68000),
          ('Guamá', 'DAGUA', 98000),
          ('Terra Firme', 'DAGUA', 65000),
          ('Jurunas', 'DABEL', 68000)
      `);
      console.log('✓ Bairros de Belém criados');

      // Criar alguns chamados de exemplo
      await sequelize.query(`
        INSERT INTO chamados (id, protocolo, categoria_id, cidadao_id, bairro_id, titulo, descricao, endereco, latitude, longitude, status, prioridade)
        VALUES 
          ('chamado-1', 'BEL-2024-0001', 1, 'user-cidadao1', 1, 'Poste apagado', 'Poste de iluminação apagado há 3 dias na Av. Presidente Vargas', 'Av. Presidente Vargas, 1234', -1.4558, -48.4902, 'aberto', 'alta'),
          ('chamado-2', 'BEL-2024-0002', 2, 'user-cidadao2', 5, 'Buraco grande', 'Buraco grande causando risco de acidentes', 'Av. Almirante Barroso, 2500', -1.4350, -48.4650, 'em_andamento', 'critica'),
          ('chamado-3', 'BEL-2024-0003', 3, 'user-cidadao1', 2, 'Lixo acumulado', 'Acúmulo de lixo no Ver-o-Peso', 'Complexo Ver-o-Peso', -1.4520, -48.5040, 'concluido', 'media')
      `);
      console.log('✓ Chamados de exemplo criados');
    } else {
      console.log('⚠ Banco já contém dados, pulando população inicial');
    }

    console.log('\n✅ Banco de dados inicializado com sucesso!');
    console.log('\n📊 Resumo:');
    console.log('   - Arquivo: backend/database.sqlite');
    console.log('   - Tabelas: usuarios, categorias, bairros, chamados');
    console.log('   - Usuários de teste criados');
    console.log('\n🔐 Login de teste:');
    console.log('   Email: pedro.almeida@email.com');
    console.log('   Senha: senha123');
    console.log('\n🚀 Agora você pode iniciar o backend com: npm run dev\n');

    process.exit(0);

  } catch (error) {
    console.error('\n❌ Erro ao inicializar banco:', error.message);
    process.exit(1);
  }
}

// Executar
initDatabase();
