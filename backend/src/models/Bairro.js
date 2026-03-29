const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Bairro = sequelize.define('Bairro', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    nome: {
        type: DataTypes.STRING,
        allowNull: false
    },
    regiao: {
        type: DataTypes.STRING
    },
    ativo: {
        type: DataTypes.BOOLEAN,
        defaultValue: true
    }
}, {
    tableName: 'bairros'
});

module.exports = Bairro;
