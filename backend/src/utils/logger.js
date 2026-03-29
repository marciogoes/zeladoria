const winston = require('winston');
const path = require('path');

// Definir níveis de log
const levels = {
    error: 0,
    warn: 1,
    info: 2,
    http: 3,
    debug: 4
};

// Definir cores
const colors = {
    error: 'red',
    warn: 'yellow',
    info: 'green',
    http: 'magenta',
    debug: 'blue'
};

winston.addColors(colors);

// Formato do log
const format = winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.colorize({ all: true }),
    winston.format.printf(
        (info) => `${info.timestamp} ${info.level}: ${info.message}`
    )
);

// Transports
const transports = [
    // Console
    new winston.transports.Console(),
    // Arquivo de erros
    new winston.transports.File({
        filename: path.join(__dirname, '../../logs/error.log'),
        level: 'error',
        format: winston.format.combine(
            winston.format.uncolorize(),
            winston.format.json()
        )
    }),
    // Arquivo geral
    new winston.transports.File({
        filename: path.join(__dirname, '../../logs/all.log'),
        format: winston.format.combine(
            winston.format.uncolorize(),
            winston.format.json()
        )
    })
];

// Criar logger
const logger = winston.createLogger({
    level: process.env.NODE_ENV === 'development' ? 'debug' : 'warn',
    levels,
    format,
    transports
});

// Stream para Morgan
logger.stream = {
    write: (message) => logger.http(message.trim())
};

module.exports = logger;
