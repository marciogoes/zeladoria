const jwt = require('jsonwebtoken');
const { Usuario } = require('../models');

const auth = async (req, res, next) => {
    try {
        // Pegar token do header
        const token = req.header('Authorization')?.replace('Bearer ', '');

        if (!token) {
            throw new Error('Token não fornecido');
        }

        // Verificar token
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret_key_zeladoria_belem');

        // Buscar usuário
        const usuario = await Usuario.findByPk(decoded.id);

        if (!usuario || !usuario.ativo) {
            throw new Error('Usuário não encontrado ou inativo');
        }

        // Adicionar usuário à requisição
        req.usuario = usuario;
        req.token = token;

        next();
    } catch (error) {
        res.status(401).json({ error: 'Por favor, autentique-se' });
    }
};

// Middleware para verificar tipo de usuário
const checkRole = (...roles) => {
    return (req, res, next) => {
        if (!req.usuario) {
            return res.status(401).json({ error: 'Não autenticado' });
        }

        if (!roles.includes(req.usuario.tipo)) {
            return res.status(403).json({ 
                error: 'Sem permissão para acessar este recurso' 
            });
        }

        next();
    };
};

module.exports = { auth, checkRole };
