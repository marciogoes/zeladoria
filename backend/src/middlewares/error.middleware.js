const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
    logger.error(`${err.name}: ${err.message}`);
    logger.error(err.stack);

    // Erro de validação do Sequelize
    if (err.name === 'SequelizeValidationError') {
        return res.status(400).json({
            error: 'Erro de validação',
            details: err.errors.map(e => ({
                field: e.path,
                message: e.message
            }))
        });
    }

    // Erro de constraint único
    if (err.name === 'SequelizeUniqueConstraintError') {
        return res.status(409).json({
            error: 'Registro já existe',
            field: err.errors[0].path
        });
    }

    // Erro de JWT
    if (err.name === 'JsonWebTokenError') {
        return res.status(401).json({
            error: 'Token inválido'
        });
    }

    if (err.name === 'TokenExpiredError') {
        return res.status(401).json({
            error: 'Token expirado'
        });
    }

    // Erro genérico
    res.status(err.status || 500).json({
        error: err.message || 'Erro interno do servidor',
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
};

module.exports = errorHandler;
