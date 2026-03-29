#!/bin/bash
# ============================================
# DOCKER ENTRYPOINT
# Sistema de Zeladoria Urbana - Belém/PA
# ============================================

set -e

echo "🚀 Iniciando Sistema de Zeladoria Urbana..."

# ==========================================
# AGUARDAR BANCO DE DADOS
# ==========================================
if [ "$DATABASE_URL" ]; then
    echo "⏳ Aguardando banco de dados..."
    
    # Extrair host do DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\).*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ -z "$DB_PORT" ]; then
        DB_PORT=5432
    fi
    
    # Aguardar até que o banco esteja disponível
    until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U zeladoria 2>/dev/null; do
        echo "⏳ Aguardando PostgreSQL em $DB_HOST:$DB_PORT..."
        sleep 2
    done
    
    echo "✅ Banco de dados disponível!"
fi

# ==========================================
# CRIAR DIRETÓRIOS NECESSÁRIOS
# ==========================================
echo "📁 Criando diretórios..."
mkdir -p uploads logs backups

# ==========================================
# EXECUTAR MIGRAÇÕES (SE NECESSÁRIO)
# ==========================================
if [ -d "migrations" ]; then
    echo "🔄 Executando migrações do banco de dados..."
    # alembic upgrade head
fi

# ==========================================
# POPULAR DADOS INICIAIS (APENAS PRIMEIRA VEZ)
# ==========================================
if [ "$POPULATE_DATA" = "true" ]; then
    echo "📊 Populando dados iniciais..."
    python seed.py || true
fi

# ==========================================
# COLETAR ARQUIVOS ESTÁTICOS (SE NECESSÁRIO)
# ==========================================
# if [ "$ENVIRONMENT" = "production" ]; then
#     echo "📦 Coletando arquivos estáticos..."
#     python manage.py collectstatic --noinput || true
# fi

# ==========================================
# HEALTH CHECK INICIAL
# ==========================================
echo "💊 Sistema pronto para health checks..."

# ==========================================
# EXECUTAR COMANDO
# ==========================================
echo "🎉 Iniciando aplicação..."
echo "📡 API: http://localhost:8001"
echo "📚 Docs: http://localhost:8001/docs"
echo ""

exec "$@"
