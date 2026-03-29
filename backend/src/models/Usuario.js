const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const bcrypt = require('bcryptjs');

const Usuario = sequelize.define('Usuario', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    nome: {
        type: DataTypes.STRING,
        allowNull: false
    },
    email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
        validate: {
            isEmail: true
        }
    },
    senha: {
        type: DataTypes.STRING,
        allowNull: false
    },
    telefone: {
        type: DataTypes.STRING
    },
    cpf: {
        type: DataTypes.STRING,
        unique: true
    },
    tipo: {
        type: DataTypes.ENUM('cidadao', 'equipe', 'gestor', 'admin'),
        defaultValue: 'cidadao'
    },
    ativo: {
        type: DataTypes.BOOLEAN,
        defaultValue: true
    },
    avatar: {
        type: DataTypes.STRING
    }
}, {
    tableName: 'usuarios',
    hooks: {
        beforeCreate: async (usuario) => {
            if (usuario.senha) {
                usuario.senha = await bcrypt.hash(usuario.senha, 10);
            }
        },
        beforeUpdate: async (usuario) => {
            if (usuario.changed('senha')) {
                usuario.senha = await bcrypt.hash(usuario.senha, 10);
            }
        }
    }
});

// Método para verificar senha
Usuario.prototype.verificarSenha = async function(senha) {
    return await bcrypt.compare(senha, this.senha);
};

// Método para serializar (não retornar senha)
Usuario.prototype.toJSON = function() {
    const values = Object.assign({}, this.get());
    delete values.senha;
    return values;
};

module.exports = Usuario;
