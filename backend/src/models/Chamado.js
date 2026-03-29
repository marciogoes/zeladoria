const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Chamado = sequelize.define('Chamado', {
    id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    protocolo: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: false
    },
    titulo: {
        type: DataTypes.STRING,
        allowNull: false
    },
    descricao: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    endereco: {
        type: DataTypes.STRING,
        allowNull: false
    },
    latitude: {
        type: DataTypes.DECIMAL(10, 8)
    },
    longitude: {
        type: DataTypes.DECIMAL(11, 8)
    },
    foto_antes: {
        type: DataTypes.STRING
    },
    foto_depois: {
        type: DataTypes.STRING
    },
    status: {
        type: DataTypes.ENUM('aberto', 'em_andamento', 'resolvido', 'cancelado'),
        defaultValue: 'aberto'
    },
    prioridade: {
        type: DataTypes.ENUM('baixa', 'media', 'alta', 'critica'),
        defaultValue: 'media'
    },
    avaliacao: {
        type: DataTypes.INTEGER,
        validate: {
            min: 1,
            max: 5
        }
    },
    comentario_avaliacao: {
        type: DataTypes.TEXT
    },
    data_resolucao: {
        type: DataTypes.DATE
    },
    usuario_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'usuarios',
            key: 'id'
        }
    },
    categoria_id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'categorias',
            key: 'id'
        }
    },
    bairro_id: {
        type: DataTypes.INTEGER,
        references: {
            model: 'bairros',
            key: 'id'
        }
    },
    responsavel_id: {
        type: DataTypes.INTEGER,
        references: {
            model: 'usuarios',
            key: 'id'
        }
    }
}, {
    tableName: 'chamados'
});

// Gerar protocolo antes de criar
Chamado.beforeCreate((chamado) => {
    if (!chamado.protocolo) {
        const timestamp = Date.now();
        const random = Math.floor(Math.random() * 1000);
        chamado.protocolo = `BEL${timestamp}${random}`;
    }
});

module.exports = Chamado;
