const { Usuario } = require('../models');

// @desc    Listar usuários
// @route   GET /api/usuarios
// @access  Private (Admin/Gestor)
const getUsuarios = async (req, res, next) => {
    try {
        const { tipo } = req.query;
        
        const where = {};
        if (tipo) where.tipo = tipo;

        const usuarios = await Usuario.findAll({
            where,
            attributes: { exclude: ['senha'] },
            order: [['nome', 'ASC']]
        });

        res.json(usuarios);
    } catch (error) {
        next(error);
    }
};

// @desc    Obter usuário por ID
// @route   GET /api/usuarios/:id
// @access  Private
const getUsuario = async (req, res, next) => {
    try {
        const usuario = await Usuario.findByPk(req.params.id, {
            attributes: { exclude: ['senha'] }
        });

        if (!usuario) {
            return res.status(404).json({ error: 'Usuário não encontrado' });
        }

        res.json(usuario);
    } catch (error) {
        next(error);
    }
};

module.exports = {
    getUsuarios,
    getUsuario
};
