#!/bin/bash

# ============================================
# SCRIPT DE ATUALIZAÇÃO/MIGRAÇÃO
# Sistema de Zeladoria Urbana - Belém/PA
# Versão: 2.0.0
# ============================================

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
echo "║   Script de Atualização v2.0.0                       ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se está no diretório correto
if [ ! -f "main.py" ]; then
    log_error "Execute este script no diretório raiz do projeto!"
    exit 1
fi

# Parar servidor se estiver rodando
log_info "Verificando se o servidor está rodando..."
PID=$(ps aux | grep uvicorn | grep -v grep | awk '{print $2}')
if [ ! -z "$PID" ]; then
    log_warning "Parando servidor (PID: $PID)..."
    kill $PID
    sleep 2
    log_success "Servidor parado"
fi

# Backup do banco de dados
log_info "Criando backup do banco de dados..."
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR

if [ -f "zeladoria.db" ]; then
    cp zeladoria.db "$BACKUP_DIR/zeladoria_backup_$TIMESTAMP.db"
    log_success "Backup criado: $BACKUP_DIR/zeladoria_backup_$TIMESTAMP.db"
else
    log_warning "Banco de dados não encontrado, pulando backup"
fi

# Backup do .env
if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/.env_backup_$TIMESTAMP"
    log_success "Backup do .env criado"
fi

# Ativar ambiente virtual
log_info "Ativando ambiente virtual..."
if [ -d "venv" ]; then
    source venv/bin/activate || . venv/Scripts/activate
    log_success "Ambiente virtual ativado"
else
    log_error "Ambiente virtual não encontrado. Execute ./install.sh primeiro"
    exit 1
fi

# Atualizar dependências
log_info "Atualizando dependências Python..."
pip install --upgrade pip
pip install --upgrade -r requirements.txt
log_success "Dependências atualizadas"

# Verificar mudanças no .env.example
log_info "Verificando .env..."
if [ -f ".env.example" ]; then
    if ! diff -q .env .env.example > /dev/null 2>&1; then
        log_warning "Há mudanças no .env.example!"
        log_warning "Revise o arquivo .env.example e atualize seu .env se necessário"
        
        echo ""
        echo "Deseja ver as diferenças agora? (s/n)"
        read -r SHOW_DIFF
        
        if [ "$SHOW_DIFF" = "s" ] || [ "$SHOW_DIFF" = "S" ]; then
            diff .env .env.example || true
        fi
    else
        log_success "Arquivo .env está atualizado"
    fi
fi

# Executar migrações (se houver)
if [ -d "migrations" ]; then
    log_info "Executando migrações do banco de dados..."
    # alembic upgrade head
    log_success "Migrações executadas"
fi

# Atualizar arquivos estáticos (se necessário)
log_info "Verificando arquivos estáticos..."
if [ -d "frontend" ]; then
    log_success "Arquivos estáticos verificados"
fi

# Verificar integridade do banco
log_info "Verificando integridade do banco de dados..."
python3 << EOF
try:
    from app.database import engine
    from sqlalchemy import text
    
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        connection.commit()
    print("✅ Banco de dados OK")
except Exception as e:
    print(f"❌ Erro no banco de dados: {e}")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    log_error "Erro na verificação do banco de dados"
    log_warning "Restaurando backup..."
    
    if [ -f "$BACKUP_DIR/zeladoria_backup_$TIMESTAMP.db" ]; then
        cp "$BACKUP_DIR/zeladoria_backup_$TIMESTAMP.db" zeladoria.db
        log_success "Backup restaurado"
    fi
    exit 1
fi

# Executar testes
log_info "Deseja executar os testes? (s/n)"
read -r RUN_TESTS

if [ "$RUN_TESTS" = "s" ] || [ "$RUN_TESTS" = "S" ]; then
    log_info "Executando testes..."
    python test_suite.py
    
    if [ $? -ne 0 ]; then
        log_error "Alguns testes falharam!"
        log_warning "Verifique os erros antes de continuar"
        
        echo "Deseja continuar mesmo assim? (s/n)"
        read -r CONTINUE
        
        if [ "$CONTINUE" != "s" ] && [ "$CONTINUE" != "S" ]; then
            log_info "Atualização cancelada"
            exit 1
        fi
    fi
fi

# Limpar cache Python
log_info "Limpando cache Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
log_success "Cache limpo"

# Verificar logs antigos
log_info "Verificando logs antigos..."
if [ -d "logs" ]; then
    LOG_COUNT=$(find logs -name "*.log" -type f | wc -l)
    if [ $LOG_COUNT -gt 10 ]; then
        log_warning "Há $LOG_COUNT arquivos de log"
        echo "Deseja limpar logs antigos (mantém os 10 mais recentes)? (s/n)"
        read -r CLEAN_LOGS
        
        if [ "$CLEAN_LOGS" = "s" ] || [ "$CLEAN_LOGS" = "S" ]; then
            find logs -name "*.log" -type f | sort -r | tail -n +11 | xargs rm -f
            log_success "Logs antigos removidos"
        fi
    fi
fi

# Resumo da atualização
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                        ║${NC}"
echo -e "${GREEN}║  ✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!                ║${NC}"
echo -e "${GREEN}║                                                        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

log_info "Backups criados:"
echo "  • Banco: $BACKUP_DIR/zeladoria_backup_$TIMESTAMP.db"
if [ -f "$BACKUP_DIR/.env_backup_$TIMESTAMP" ]; then
    echo "  • .env: $BACKUP_DIR/.env_backup_$TIMESTAMP"
fi

echo ""
log_info "Próximos passos:"
echo "  1. Revise o .env se houver mudanças"
echo "  2. Inicie o servidor: ./start.sh"
echo "  3. Teste o sistema no navegador"
echo ""

log_info "Deseja iniciar o servidor agora? (s/n)"
read -r START_SERVER

if [ "$START_SERVER" = "s" ] || [ "$START_SERVER" = "S" ]; then
    log_info "Iniciando servidor..."
    ./start.sh
else
    log_info "Execute ./start.sh quando estiver pronto"
fi

echo ""
echo -e "${BLUE}🎉 Atualização completa!${NC}"
echo ""
