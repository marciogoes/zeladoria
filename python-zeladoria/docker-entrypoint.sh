#!/bin/bash
# ============================================
# DOCKER ENTRYPOINT
# Sistema de Zeladoria Urbana - Belém/PA
# ============================================

set -e

echo "🚀 Iniciando Sistema de Zeladoria Urbana..."

# ==========================================
# AGUARDAR BANCO DE DADOS (usando Python)
# ==========================================
if [ "$DATABASE_URL" ]; then
    echo "⏳ Aguardando banco de dados..."
    
    MAX_TRIES=30
    COUNT=0
    until python -c "
import sys, os
url = os.environ.get('DATABASE_URL', '')
if not url or 'sqlite' in url:
    sys.exit(0)
try:
    import psycopg2
    conn = psycopg2.connect(url, connect_timeout=3)
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; do
        COUNT=$((COUNT+1))
        if [ $COUNT -ge $MAX_TRIES ]; then
            echo "⚠️  Banco não respondeu após $MAX_TRIES tentativas. Iniciando mesmo assim..."
            break
        fi
        echo "⏳ Aguardando banco de dados... ($COUNT/$MAX_TRIES)"
        sleep 2
    done
    
    echo "✅ Banco de dados disponível (ou SQLite)!"
fi

# ==========================================
# CRIAR DIRETÓRIOS NECESSÁRIOS
# ==========================================
echo "📁 Criando diretórios..."
mkdir -p uploads logs backups

# ==========================================
# POPULAR DADOS INICIAIS (APENAS PRIMEIRA VEZ)
# ==========================================
if [ "$POPULATE_DATA" = "true" ]; then
    echo "📊 Populando dados iniciais..."
    python seed.py || true
fi

# ==========================================
# EXECUTAR COMANDO
# ==========================================
echo "🎉 Iniciando aplicação..."
echo "📡 API: http://localhost:${PORT:-8001}"
echo "📚 Docs: http://localhost:${PORT:-8001}/docs"
echo ""

exec "$@"
