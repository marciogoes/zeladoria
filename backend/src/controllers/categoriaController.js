const { Categoria } = require('../models');

// @desc    Listar categorias
// @route   GET /api/categorias
// @access  Public
const getCategorias = async (req, res, next) => {
    try {
        const categorias = await Categoria.findAll({
            where: { ativo: true },
            order: [['nome', 'ASC']]
        });

        res.json(categorias);
    } catch (error) {
        next(error);
    }
};

// @desc    Criar categoria
// @route   POST /api/categorias
// @access  Private (Admin/Gestor)
const createCategoria = async (req, res, next) => {
    try {
        const { nome, descricao, icone, cor, sla_horas } = req.body;

        const categoria = await Categoria.create({
            nome,
            descricao,
            icone,
            cor,
            sla_horas
        });

        res.status(201).json(categoria);
    } catch (error) {
        next(error);
    }
};

module.exports = {
    getCategorias,
    createCategoria
};
