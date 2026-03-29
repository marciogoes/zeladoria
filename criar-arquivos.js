const fs = require('fs');
const path = require('path');

// Script para criar todos os arquivos restantes do projeto
console.log('🚀 Iniciando criação dos arquivos restantes...\n');

const BASE_PATH = __dirname;

// Definir todos os arquivos que precisam ser criados
const files = {
  // Backend - app.js
  'backend/src/app.js': `/**
 * SISTEMA DE ZELADORIA URBANA - BELÉM/PA
 * Configuração do Express App
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');
const rateLimit = require('express-rate-limit');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const path = require('path');

const logger = require('./utils/logger');
const errorMiddleware = require('./middlewares/error.middleware');

// Importar rotas
const authRoutes = require('./routes/auth.routes');
const chamadosRoutes = require('./routes/chamados.routes');
const categoriasRoutes = require('./routes/categorias.routes');
const bairrosRoutes = require('./routes/bairros.routes');

const app = express();

// Segurança
app.use(helmet({
  crossOriginResourcePolicy: { policy: "cross-origin" }
}));

// CORS
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true
}));

// Body parser
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Compressão
app.use(compression());

// Logging
if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
}

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Muitas requisições deste IP, tente novamente mais tarde.'
});

app.use('/api/', limiter);

// Servir arquivos estáticos
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Rota raiz
app.get('/', (req, res) => {
  res.json({
    message: 'Sistema de Zeladoria Urbana - Belém/PA',
    version: '1.0.0',
    status: 'Online'
  });
});

// Rotas da API
app.use('/api/auth', authRoutes);
app.use('/api/chamados', chamadosRoutes);
app.use('/api/categorias', categoriasRoutes);
app.use('/api/bairros', bairrosRoutes);

// Middleware de erro global
app.use(errorMiddleware);

module.exports = app;
`,

  // Backend - database.js
  'backend/src/config/database.js': `const { Sequelize } = require('sequelize');
const logger = require('../utils/logger');

const sequelize = new Sequelize(
  process.env.DB_NAME || 'belem_zeladoria',
  process.env.DB_USER || 'zeladoria',
  process.env.DB_PASSWORD || 'zeladoria123',
  {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    dialect: 'postgres',
    logging: process.env.NODE_ENV === 'development' ? (msg) => logger.debug(msg) : false,
    pool: {
      max: 10,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
);

module.exports = { sequelize };
`,

  // Backend - logger.js
  'backend/src/utils/logger.js': `const winston = require('winston');
const path = require('path');

const customFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.printf(({ timestamp, level, message, stack }) => {
    const msg = \`\${timestamp} [\${level.toUpperCase()}]: \${message}\`;
    return stack ? \`\${msg}\\n\${stack}\` : msg;
  })
);

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: customFormat,
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        customFormat
      )
    }),
    new winston.transports.File({
      filename: path.join(__dirname, '../../logs/error.log'),
      level: 'error',
      maxsize: 5242880,
      maxFiles: 5
    }),
    new winston.transports.File({
      filename: path.join(__dirname, '../../logs/combined.log'),
      maxsize: 5242880,
      maxFiles: 5
    })
  ]
});

module.exports = logger;
`,

  // Backend - error.middleware.js
  'backend/src/middlewares/error.middleware.js': `module.exports = (err, req, res, next) => {
  console.error(err.stack);
  
  res.status(err.statusCode || 500).json({
    success: false,
    message: err.message || 'Erro interno do servidor',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};
`,

  // Frontend - package.json
  'frontend/package.json': `{
  "name": "belem-zeladoria-frontend",
  "version": "1.0.0",
  "description": "Sistema de Zeladoria Urbana - Frontend para Prefeitura de Belém/PA",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "axios": "^1.6.2",
    "recharts": "^2.10.3",
    "lucide-react": "^0.294.0",
    "date-fns": "^2.30.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "tailwindcss": "^3.3.6",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0"
  }
}
`
};

// Função para criar arquivo
function createFile(filePath, content) {
  const fullPath = path.join(BASE_PATH, filePath);
  const dir = path.dirname(fullPath);
  
  // Criar diretório se não existir
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // Escrever arquivo
  fs.writeFileSync(fullPath, content, 'utf8');
  console.log(`✓ Criado: ${filePath}`);
}

// Criar todos os arquivos
console.log('Criando arquivos...\n');

for (const [filePath, content] of Object.entries(files)) {
  try {
    createFile(filePath, content);
  } catch (error) {
    console.error(`✗ Erro ao criar ${filePath}:`, error.message);
  }
}

console.log('\n✅ Arquivos criados com sucesso!');
console.log('\n📝 Próximos passos:');
console.log('1. Instale as dependências: npm install (em backend e frontend)');
console.log('2. Inicie o servidor: npm run dev');
console.log('\n🚀 Boa sorte!');
