const { Chamado, Usuario, Categoria, Bairro } = require('../models');
const { Op } = require('sequelize');

// @desc    Listar chamados
// @route   GET /api/chamados
// @access  Private
const getChamados = async (req, res, next) => {
    try {
        const { status, prioridade, categoria_id, bairro_id, search } = req.query;
        
        const where = {};

        // Filtros
        if (status) where.status = status;
        if (prioridade) where.prioridade = prioridade;
        if (categoria_id) where.categoria_id = categoria_id;
        if (bairro_id) where.bairro_id = bairro_id;

        // Busca por protocolo ou título
        if (search) {
            where[Op.or] = [
                { protocolo: { [Op.like]: `%${search}%` } },
                { titulo: { [Op.like]: `%${search}%` } }
            ];
        }

        // Se usuário é cidadão, mostrar apenas seus chamados
        if (req.usuario.tipo === 'cidadao') {
            where.usuario_id = req.usuario.id;
        }

        const chamados = await Chamado.findAll({
            where,
            include: [
                { model: Usuario, as: 'usuario', attributes: ['id', 'nome', 'email'] },
                { model: Usuario, as: 'responsavel', attributes: ['id', 'nome'] },
                { model: Categoria, as: 'categoria', attributes: ['id', 'nome', 'icone', 'cor'] },
                { model: Bairro, as: 'bairro', attributes: ['id', 'nome'] }
            ],
            order: [['created_at', 'DESC']]
        });

        res.json(chamados);
    } catch (error) {
        next(error);
    }
};

// @desc    Obter chamado por ID
// @route   GET /api/chamados/:id
// @access  Private
const getChamado = async (req, res, next) => {
    try {
        const chamado = await Chamado.findByPk(req.params.id, {
            include: [
                { model: Usuario, as: 'usuario', attributes: ['id', 'nome', 'email', 'telefone'] },
                { model: Usuario, as: 'responsavel', attributes: ['id', 'nome'] },
                { model: Categoria, as: 'categoria' },
                { model: Bairro, as: 'bairro' }
            ]
        });

        if (!chamado) {
            return res.status(404).json({ error: 'Chamado não encontrado' });
        }

        // Cidadão só pode ver seus próprios chamados
        if (req.usuario.tipo === 'cidadao' && chamado.usuario_id !== req.usuario.id) {
            return res.status(403).json({ error: 'Sem permissão' });
        }

        res.json(chamado);
    } catch (error) {
        next(error);
    }
};

// @desc    Criar chamado
// @route   POST /api/chamados
// @access  Private
const createChamado = async (req, res, next) => {
    try {
        const {
            titulo,
            descricao,
            endereco,
            latitude,
            longitude,
            categoria_id,
            bairro_id
        } = req.body;

        // Validar campos obrigatórios
        if (!titulo || !descricao || !endereco || !categoria_id) {
            return res.status(400).json({ 
                error: 'Título, descrição, endereço e categoria são obrigatórios' 
            });
        }

        const chamado = await Chamado.create({
            titulo,
            descricao,
            endereco,
            latitude,
            longitude,
            categoria_id,
            bairro_id,
            usuario_id: req.usuario.id,
            foto_antes: req.file ? `/uploads/${req.file.filename}` : null
        });

        // Recarregar com relações
        await chamado.reload({
            include: [
                { model: Usuario, as: 'usuario', attributes: ['id', 'nome', 'email'] },
                { model: Categoria, as: 'categoria' },
                { model: Bairro, as: 'bairro' }
            ]
        });

        res.status(201).json(chamado);
    } catch (error) {
        next(error);
    }
};

// @desc    Atualizar chamado
// @route   PUT /api/chamados/:id
// @access  Private
const updateChamado = async (req, res, next) => {
    try {
        const chamado = await Chamado.findByPk(req.params.id);

        if (!chamado) {
            return res.status(404).json({ error: 'Chamado não encontrado' });
        }

        // Cidadão não pode atualizar após criar
        if (req.usuario.tipo === 'cidadao') {
            return res.status(403).json({ error: 'Sem permissão para atualizar' });
        }

        const { status, prioridade, responsavel_id } = req.body;

        if (status) chamado.status = status;
        if (prioridade) chamado.prioridade = prioridade;
        if (responsavel_id) chamado.responsavel_id = responsavel_id;

        // Se foi resolvido, registrar data
        if (status === 'resolvido' && !chamado.data_resolucao) {
            chamado.data_resolucao = new Date();
        }

        // Foto depois
        if (req.file) {
            chamado.foto_depois = `/uploads/${req.file.filename}`;
        }

        await chamado.save();

        await chamado.reload({
            include: [
                { model: Usuario, as: 'usuario', attributes: ['id', 'nome', 'email'] },
                { model: Usuario, as: 'responsavel', attributes: ['id', 'nome'] },
                { model: Categoria, as: 'categoria' },
                { model: Bairro, as: 'bairro' }
            ]
        });

        res.json(chamado);
    } catch (error) {
        next(error);
    }
};

// @desc    Avaliar chamado
// @route   POST /api/chamados/:id/avaliar
// @access  Private
const avaliarChamado = async (req, res, next) => {
    try {
        const { avaliacao, comentario_avaliacao } = req.body;

        const chamado = await Chamado.findByPk(req.params.id);

        if (!chamado) {
            return res.status(404).json({ error: 'Chamado não encontrado' });
        }

        // Apenas o criador pode avaliar
        if (chamado.usuario_id !== req.usuario.id) {
            return res.status(403).json({ error: 'Sem permissão' });
        }

        // Apenas chamados resolvidos podem ser avaliados
        if (chamado.status !== 'resolvido') {
            return res.status(400).json({ error: 'Apenas chamados resolvidos podem ser avaliados' });
        }

        chamado.avaliacao = avaliacao;
        chamado.comentario_avaliacao = comentario_avaliacao;

        await chamado.save();

        res.json(chamado);
    } catch (error) {
        next(error);
    }
};

module.exports = {
    getChamados,
    getChamado,
    createChamado,
    updateChamado,
    avaliarChamado
};
