const { Chamado, Usuario, Categoria, Bairro } = require('../models');
const { Op, fn, col } = require('sequelize');

// @desc    Dashboard com KPIs
// @route   GET /api/relatorios/dashboard
// @access  Private (Gestor/Admin)
const getDashboard = async (req, res, next) => {
    try {
        // Total de chamados
        const totalChamados = await Chamado.count();

        // Chamados por status
        const porStatus = await Chamado.findAll({
            attributes: [
                'status',
                [fn('COUNT', col('id')), 'total']
            ],
            group: ['status']
        });

        // Chamados por prioridade
        const porPrioridade = await Chamado.findAll({
            attributes: [
                'prioridade',
                [fn('COUNT', col('id')), 'total']
            ],
            group: ['prioridade']
        });

        // Top categorias
        const topCategorias = await Chamado.findAll({
            attributes: [
                [fn('COUNT', col('Chamado.id')), 'total']
            ],
            include: [{
                model: Categoria,
                as: 'categoria',
                attributes: ['id', 'nome', 'icone', 'cor']
            }],
            group: ['categoria.id'],
            order: [[fn('COUNT', col('Chamado.id')), 'DESC']],
            limit: 5
        });

        // Top bairros
        const topBairros = await Chamado.findAll({
            attributes: [
                [fn('COUNT', col('Chamado.id')), 'total']
            ],
            include: [{
                model: Bairro,
                as: 'bairro',
                attributes: ['id', 'nome']
            }],
            where: {
                bairro_id: {
                    [Op.not]: null
                }
            },
            group: ['bairro.id'],
            order: [[fn('COUNT', col('Chamado.id')), 'DESC']],
            limit: 5
        });

        // Chamados recentes
        const recentes = await Chamado.findAll({
            include: [
                { model: Usuario, as: 'usuario', attributes: ['nome'] },
                { model: Categoria, as: 'categoria', attributes: ['nome', 'icone'] }
            ],
            order: [['created_at', 'DESC']],
            limit: 10
        });

        // Média de avaliação
        const avaliacaoMedia = await Chamado.findOne({
            attributes: [[fn('AVG', col('avaliacao')), 'media']],
            where: {
                avaliacao: {
                    [Op.not]: null
                }
            }
        });

        res.json({
            totalChamados,
            porStatus: porStatus.map(s => ({
                status: s.status,
                total: s.dataValues.total
            })),
            porPrioridade: porPrioridade.map(p => ({
                prioridade: p.prioridade,
                total: p.dataValues.total
            })),
            topCategorias: topCategorias.map(c => ({
                categoria: c.categoria,
                total: c.dataValues.total
            })),
            topBairros: topBairros.map(b => ({
                bairro: b.bairro,
                total: b.dataValues.total
            })),
            recentes,
            avaliacaoMedia: parseFloat(avaliacaoMedia?.dataValues.media || 0).toFixed(1)
        });
    } catch (error) {
        next(error);
    }
};

module.exports = {
    getDashboard
};
