const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Categoria = sequelize.define('Categoria', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    nome: {
        type: DataTypes.STRING,
        allowNull: false
    },
    descricao: {
        type: DataTypes.TEXT
    },
    icone: {
        type: DataTypes.STRING
    },
    cor: {
        type: DataTypes.STRING,
        defaultValue: '#667eea'
    },
    ativo: {
        type: DataTypes.BOOLEAN,
        defaultValue: true
    },
    sla_horas: {
        type: DataTypes.INTEGER,
        defaultValue: 72,
        comment: 'Prazo em horas para resolução'
    }
}, {
    tableName: 'categorias'
});

module.exports = Categoria;
