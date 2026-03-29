const { Sequelize } = require('sequelize');
const logger = require('../utils/logger');

// Configuração do Sequelize com SQLite
const sequelize = new Sequelize({
    dialect: 'sqlite',
    storage: './database.sqlite',
    logging: (msg) => logger.debug(msg),
    define: {
        timestamps: true,
        underscored: true,
        createdAt: 'created_at',
        updatedAt: 'updated_at'
    }
});

// Testar conexão
const testConnection = async () => {
    try {
        await sequelize.authenticate();
        logger.info('✓ Conexão com banco de dados estabelecida');
        return true;
    } catch (error) {
        logger.error('✗ Erro ao conectar ao banco de dados:', error);
        return false;
    }
};

// Sincronizar modelos (criar tabelas)
const syncDatabase = async (force = false) => {
    try {
        await sequelize.sync({ force, alter: !force });
        logger.info('✓ Tabelas sincronizadas com sucesso');
        return true;
    } catch (error) {
        logger.error('✗ Erro ao sincronizar tabelas:', error);
        return false;
    }
};

module.exports = {
    sequelize,
    testConnection,
    syncDatabase
};
