const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');
const logger = require('./utils/logger');
const errorHandler = require('./middlewares/error.middleware');

// Importar rotas
const authRoutes = require('./routes/auth.routes');
const chamadosRoutes = require('./routes/chamados.routes');
const categoriasRoutes = require('./routes/categorias.routes');
const bairrosRoutes = require('./routes/bairros.routes');
const usuariosRoutes = require('./routes/usuarios.routes');
const relatoriosRoutes = require('./routes/relatorios.routes');

const app = express();

// Middlewares de segurança
app.use(helmet());
app.use(cors({
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    credentials: true
}));

// Logging
if (process.env.NODE_ENV === 'development') {
    app.use(morgan('dev'));
} else {
    app.use(morgan('combined', { stream: logger.stream }));
}

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Servir arquivos estáticos (uploads)
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// Health check
app.get('/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// Rota raiz
app.get('/', (req, res) => {
    res.json({
        message: '🏛️ Sistema de Zeladoria Urbana - Belém/PA',
        version: '1.0.0',
        endpoints: {
            health: '/health',
            docs: '/api-docs',
            api: '/api'
        }
    });
});

// Rotas da API
app.use('/api/auth', authRoutes);
app.use('/api/chamados', chamadosRoutes);
app.use('/api/categorias', categoriasRoutes);
app.use('/api/bairros', bairrosRoutes);
app.use('/api/usuarios', usuariosRoutes);
app.use('/api/relatorios', relatoriosRoutes);

// Middleware de erro (deve ser o último)
app.use(errorHandler);

// Rota 404
app.use((req, res) => {
    res.status(404).json({ 
        error: 'Endpoint não encontrado',
        path: req.path 
    });
});

module.exports = app;
