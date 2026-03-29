const jwt = require('jsonwebtoken');
const { Usuario } = require('../models');

// Gerar JWT
const gerarToken = (id) => {
    return jwt.sign({ id }, process.env.JWT_SECRET || 'secret_key_zeladoria_belem', {
        expiresIn: '30d'
    });
};

// @desc    Registrar novo usuário
// @route   POST /api/auth/register
// @access  Public
const register = async (req, res, next) => {
    try {
        const { nome, email, senha, telefone, cpf, tipo } = req.body;

        // Verificar se usuário já existe
        const usuarioExiste = await Usuario.findOne({ where: { email } });
        if (usuarioExiste) {
            return res.status(400).json({ error: 'Email já cadastrado' });
        }

        // Criar usuário
        const usuario = await Usuario.create({
            nome,
            email,
            senha,
            telefone,
            cpf,
            tipo: tipo || 'cidadao'
        });

        // Gerar token
        const token = gerarToken(usuario.id);

        res.status(201).json({
            usuario,
            token
        });
    } catch (error) {
        next(error);
    }
};

// @desc    Login de usuário
// @route   POST /api/auth/login
// @access  Public
const login = async (req, res, next) => {
    try {
        const { email, senha } = req.body;

        // Validar dados
        if (!email || !senha) {
            return res.status(400).json({ error: 'Por favor, forneça email e senha' });
        }

        // Buscar usuário
        const usuario = await Usuario.findOne({ where: { email } });
        if (!usuario) {
            return res.status(401).json({ error: 'Credenciais inválidas' });
        }

        // Verificar se está ativo
        if (!usuario.ativo) {
            return res.status(401).json({ error: 'Usuário inativo' });
        }

        // Verificar senha
        const senhaCorreta = await usuario.verificarSenha(senha);
        if (!senhaCorreta) {
            return res.status(401).json({ error: 'Credenciais inválidas' });
        }

        // Gerar token
        const token = gerarToken(usuario.id);

        res.json({
            usuario,
            token
        });
    } catch (error) {
        next(error);
    }
};

// @desc    Obter usuário autenticado
// @route   GET /api/auth/me
// @access  Private
const getMe = async (req, res) => {
    res.json(req.usuario);
};

// @desc    Atualizar perfil
// @route   PUT /api/auth/me
// @access  Private
const updateMe = async (req, res, next) => {
    try {
        const { nome, telefone } = req.body;

        const usuario = await Usuario.findByPk(req.usuario.id);
        
        if (nome) usuario.nome = nome;
        if (telefone) usuario.telefone = telefone;

        await usuario.save();

        res.json(usuario);
    } catch (error) {
        next(error);
    }
};

module.exports = {
    register,
    login,
    getMe,
    updateMe
};
