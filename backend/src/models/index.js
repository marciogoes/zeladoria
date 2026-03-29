const Usuario = require('./Usuario');
const Categoria = require('./Categoria');
const Bairro = require('./Bairro');
const Chamado = require('./Chamado');

// Definir relações

// Chamado pertence a Usuario (criador)
Chamado.belongsTo(Usuario, {
    foreignKey: 'usuario_id',
    as: 'usuario'
});

// Chamado pertence a Usuario (responsável)
Chamado.belongsTo(Usuario, {
    foreignKey: 'responsavel_id',
    as: 'responsavel'
});

// Chamado pertence a Categoria
Chamado.belongsTo(Categoria, {
    foreignKey: 'categoria_id',
    as: 'categoria'
});

// Chamado pertence a Bairro
Chamado.belongsTo(Bairro, {
    foreignKey: 'bairro_id',
    as: 'bairro'
});

// Usuario tem muitos Chamados
Usuario.hasMany(Chamado, {
    foreignKey: 'usuario_id',
    as: 'chamados'
});

// Categoria tem muitos Chamados
Categoria.hasMany(Chamado, {
    foreignKey: 'categoria_id',
    as: 'chamados'
});

// Bairro tem muitos Chamados
Bairro.hasMany(Chamado, {
    foreignKey: 'bairro_id',
    as: 'chamados'
});

module.exports = {
    Usuario,
    Categoria,
    Bairro,
    Chamado
};
