const { Bairro } = require('../models');

// @desc    Listar bairros
// @route   GET /api/bairros
// @access  Public
const getBairros = async (req, res, next) => {
    try {
        const bairros = await Bairro.findAll({
            where: { ativo: true },
            order: [['nome', 'ASC']]
        });

        res.json(bairros);
    } catch (error) {
        next(error);
    }
};

module.exports = {
    getBairros
};
