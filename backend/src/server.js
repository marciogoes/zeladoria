/**
 * SISTEMA DE ZELADORIA URBANA - BELÉM/PA
 * Backend Server - Entry Point
 */

require('dotenv').config();
const app = require('./app');
const { sequelize } = require('./config/database');
const logger = require('./utils/logger');
const http = require('http');
const socketIO = require('socket.io');

const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';

// Criar servidor HTTP
const server = http.createServer(app);

// Configurar Socket.IO para notificações em tempo real
const io = socketIO(server, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:5173',
    methods: ['GET', 'POST'],
    credentials: true
  }
});

// Configurar eventos Socket.IO
io.on('connection', (socket) => {
  logger.info(`Cliente conectado: ${socket.id}`);

  socket.on('join-room', (userId) => {
    socket.join(`user-${userId}`);
    logger.info(`Usuário ${userId} entrou na sala`);
  });

  socket.on('disconnect', () => {
    logger.info(`Cliente desconectado: ${socket.id}`);
  });
});

// Disponibilizar io globalmente
app.set('io', io);

// Função para iniciar o servidor
async function startServer() {
  try {
    // Testar conexão com o banco de dados
    await sequelize.authenticate();
    logger.info('✓ Conexão com banco de dados estabelecida com sucesso');

    // Sincronizar models (apenas em desenvolvimento)
    if (NODE_ENV === 'development') {
      await sequelize.sync({ alter: false });
      logger.info('✓ Models sincronizados com banco de dados');
    }

    // Iniciar servidor
    server.listen(PORT, () => {
      logger.info(`
╔════════════════════════════════════════════════════════╗
║                                                        ║
║     🏛️  SISTEMA DE ZELADORIA URBANA - BELÉM/PA        ║
║                                                        ║
║     Ambiente: ${NODE_ENV.padEnd(40)}║
║     Servidor rodando na porta: ${PORT.toString().padEnd(27)}║
║     URL: http://localhost:${PORT.toString().padEnd(31)}║
║     API Docs: http://localhost:${PORT}/api-docs${' '.repeat(16)}║
║                                                        ║
║     Status: ✓ Online e funcionando                    ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
      `);
    });

  } catch (error) {
    logger.error('Erro ao iniciar servidor:', error);
    process.exit(1);
  }
}

// Tratamento de erros não capturados
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
  if (NODE_ENV === 'production') {
    process.exit(1);
  }
});

process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM recebido. Encerrando servidor graciosamente...');
  server.close(async () => {
    await sequelize.close();
    logger.info('Servidor encerrado');
    process.exit(0);
  });
});

process.on('SIGINT', async () => {
  logger.info('SIGINT recebido. Encerrando servidor graciosamente...');
  server.close(async () => {
    await sequelize.close();
    logger.info('Servidor encerrado');
    process.exit(0);
  });
});

// Iniciar servidor
startServer();

module.exports = { server, io };
