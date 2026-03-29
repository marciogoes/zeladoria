#!/bin/bash

# ========================================
# Script de Instalação Automatizada
# Sistema de Zeladoria Urbana - Belém/PA
# Versão: 2.0.0
# ========================================

set -e  # Para em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║   Sistema de Zeladoria Urbana - Belém/PA             ║"
echo "║   Instalação Automatizada v2.0.0                     ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar Python
log_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log_success "Python $PYTHON_VERSION encontrado"

# Verificar pip
log_info "Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    log_error "pip3 não encontrado. Instalando..."
    python3 -m ensurepip --upgrade
fi
log_success "pip encontrado"

# Criar ambiente virtual
log_info "Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    log_success "Ambiente virtual criado"
else
    log_warning "Ambiente virtual já existe"
fi

# Ativar ambiente virtual
log_info "Ativando ambiente virtual..."
source venv/bin/activate || . venv/Scripts/activate
log_success "Ambiente virtual ativado"

# Instalar dependências
log_info "Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt
log_success "Dependências instaladas"

# Criar diretórios necessários
log_info "Criando estrutura de diretórios..."
mkdir -p uploads
mkdir -p logs
mkdir -p backups
log_success "Diretórios criados"

# Configurar .env
log_info "Configurando arquivo .env..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_success "Arquivo .env criado a partir do .env.example"
        log_warning "IMPORTANTE: Edite o arquivo .env com suas configurações!"
    else
        cat > .env << EOF
# Configurações do Banco de Dados
DATABASE_URL=sqlite:///./zeladoria.db

# Segurança
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')

# API
API_URL=http://localhost:8001

# Ambiente
ENVIRONMENT=development
DEBUG=True

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8001

# Uploads
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=5242880

# Logs
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
EOF
        log_success "Arquivo .env criado com configurações padrão"
    fi
else
    log_warning "Arquivo .env já existe, mantendo configurações atuais"
fi

# Inicializar banco de dados
log_info "Inicializando banco de dados..."
if [ ! -f "zeladoria.db" ]; then
    python3 << EOF
from app.database import engine, Base
from app.models import *

Base.metadata.create_all(bind=engine)
print("Banco de dados criado com sucesso!")
EOF
    log_success "Banco de dados criado"
else
    log_warning "Banco de dados já existe"
fi

# Popular dados de teste
log_info "Deseja popular o banco com dados de teste? (s/n)"
read -r POPULATE

if [ "$POPULATE" = "s" ] || [ "$POPULATE" = "S" ]; then
    log_info "Populando banco de dados..."
    python3 seed.py
    log_success "Dados de teste inseridos"
fi

# Verificar Node.js (opcional para frontend)
log_info "Verificando Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    log_success "Node.js $NODE_VERSION encontrado"
    
    # Frontend (se existir)
    if [ -d "frontend-react" ]; then
        log_info "Instalando dependências do frontend..."
        cd frontend-react
        npm install
        cd ..
        log_success "Dependências do frontend instaladas"
    fi
else
    log_warning "Node.js não encontrado (opcional para frontend React)"
fi

# Criar script de inicialização
log_info "Criando script de inicialização..."
cat > start.sh << 'EOF'
#!/bin/bash

echo "🚀 Iniciando Sistema de Zeladoria Urbana..."

# Ativar ambiente virtual
source venv/bin/activate || . venv/Scripts/activate

# Iniciar backend
echo "📡 Iniciando backend na porta 8001..."
uvicorn main:app --reload --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

echo "✅ Backend iniciado (PID: $BACKEND_PID)"
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║  Sistema de Zeladoria Urbana - Pronto!        ║"
echo "╠════════════════════════════════════════════════╣"
echo "║                                                ║"
echo "║  🌐 Frontend: http://localhost:8001/static/   ║"
echo "║  📡 API: http://localhost:8001/api            ║"
echo "║  📚 Docs: http://localhost:8001/docs          ║"
echo "║                                                ║"
echo "║  👤 Login de Teste (Gestor):                  ║"
echo "║  Email: maria.santos@belem.pa.gov.br          ║"
echo "║  Senha: senha123                              ║"
echo "║                                                ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "Pressione Ctrl+C para parar o servidor"

# Aguardar interrupção
wait $BACKEND_PID
EOF

chmod +x start.sh
log_success "Script de inicialização criado (./start.sh)"

# Criar script de parada
log_info "Criando script de parada..."
cat > stop.sh << 'EOF'
#!/bin/bash

echo "🛑 Parando Sistema de Zeladoria Urbana..."

# Encontrar e matar processo do uvicorn
PID=$(ps aux | grep uvicorn | grep -v grep | awk '{print $2}')

if [ ! -z "$PID" ]; then
    kill $PID
    echo "✅ Backend parado (PID: $PID)"
else
    echo "⚠️  Backend não está rodando"
fi
EOF

chmod +x stop.sh
log_success "Script de parada criado (./stop.sh)"

# Criar script de backup
log_info "Criando script de backup..."
cat > backup.sh << 'EOF'
#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups"
BACKUP_FILE="$BACKUP_DIR/zeladoria_backup_$TIMESTAMP.tar.gz"

echo "💾 Criando backup..."

# Criar diretório de backups se não existir
mkdir -p $BACKUP_DIR

# Fazer backup
tar -czf $BACKUP_FILE \
    zeladoria.db \
    .env \
    uploads/ \
    logs/ \
    --exclude='logs/*.log' 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Backup criado: $BACKUP_FILE"
    
    # Manter apenas os últimos 7 backups
    ls -t $BACKUP_DIR/zeladoria_backup_*.tar.gz | tail -n +8 | xargs rm -f 2>/dev/null
    echo "🗑️  Backups antigos removidos (mantidos últimos 7)"
else
    echo "❌ Erro ao criar backup"
    exit 1
fi
EOF

chmod +x backup.sh
log_success "Script de backup criado (./backup.sh)"

# Criar cron job para backup (opcional)
log_info "Deseja configurar backup automático diário? (s/n)"
read -r CRON_BACKUP

if [ "$CRON_BACKUP" = "s" ] || [ "$CRON_BACKUP" = "S" ]; then
    CURRENT_DIR=$(pwd)
    (crontab -l 2>/dev/null; echo "0 2 * * * cd $CURRENT_DIR && ./backup.sh >> logs/backup.log 2>&1") | crontab -
    log_success "Backup automático configurado (diariamente às 2h)"
fi

# Testes básicos
log_info "Executando testes básicos..."

# Testar importação de módulos
python3 << EOF
try:
    from app.main import app
    from app.database import engine
    from app.models import Usuario, Chamado, Categoria
    print("✅ Todos os módulos importados com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar módulos: {e}")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    log_success "Testes básicos passaram"
else
    log_error "Testes básicos falharam"
    exit 1
fi

# Resumo final
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                        ║${NC}"
echo -e "${GREEN}║  ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!                 ║${NC}"
echo -e "${GREEN}║                                                        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
log_info "Próximos passos:"
echo ""
echo "  1. Edite o arquivo .env se necessário"
echo "  2. Execute: ./start.sh"
echo "  3. Acesse: http://localhost:8001/static/index.html"
echo "  4. Login: maria.santos@belem.pa.gov.br / senha123"
echo ""
log_info "Scripts disponíveis:"
echo "  • ./start.sh   - Iniciar o sistema"
echo "  • ./stop.sh    - Parar o sistema"
echo "  • ./backup.sh  - Fazer backup manual"
echo ""
log_info "Documentação:"
echo "  • INDEX.md - Índice da documentação"
echo "  • QUICK_REFERENCE.md - Referência rápida"
echo "  • RESUMO_CONSOLIDADO.md - Visão geral completa"
echo ""
echo -e "${BLUE}🎉 Sistema pronto para uso!${NC}"
echo ""
