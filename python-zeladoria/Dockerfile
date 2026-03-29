# ============================================
# DOCKERFILE - SISTEMA DE ZELADORIA URBANA
# Belém do Pará - Versão 2.0.0
# ============================================

# ==========================================
# ESTÁGIO 1: BUILD
# ==========================================
FROM python:3.11-slim as builder

# Metadados
LABEL maintainer="Prefeitura de Belém <contato@belem.pa.gov.br>"
LABEL description="Sistema de Zeladoria Urbana - Belém/PA"
LABEL version="2.0.0"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache de layer)
COPY requirements.txt .

# Criar ambiente virtual e instalar dependências
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# ESTÁGIO 2: PRODUÇÃO
# ==========================================
FROM python:3.11-slim

# Instalar apenas dependências de runtime necessárias
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd -m -u 1000 zeladoria && \
    mkdir -p /app /app/uploads /app/logs /app/backups && \
    chown -R zeladoria:zeladoria /app

# Definir diretório de trabalho
WORKDIR /app

# Copiar ambiente virtual do estágio de build
COPY --from=builder /opt/venv /opt/venv

# Copiar código da aplicação
COPY --chown=zeladoria:zeladoria . .

# Definir variáveis de ambiente
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8001

# Expor porta
EXPOSE 8001

# Mudar para usuário não-root
USER zeladoria

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Script de inicialização
COPY --chown=zeladoria:zeladoria docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Comando padrão
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

# ==========================================
# INSTRUÇÕES DE BUILD E USO
# ==========================================
#
# Build da imagem:
#   docker build -t zeladoria-urbana:2.0.0 .
#   docker build -t zeladoria-urbana:latest .
#
# Executar container:
#   docker run -d \
#     --name zeladoria \
#     -p 8001:8001 \
#     -e DATABASE_URL=sqlite:///./zeladoria.db \
#     -e SECRET_KEY=sua-chave-secreta \
#     -v $(pwd)/uploads:/app/uploads \
#     -v $(pwd)/logs:/app/logs \
#     zeladoria-urbana:latest
#
# Ver logs:
#   docker logs -f zeladoria
#
# Acessar shell do container:
#   docker exec -it zeladoria bash
#
# Parar container:
#   docker stop zeladoria
#
# Remover container:
#   docker rm zeladoria
#
# ==========================================
# MULTI-STAGE BUILD PARA OTIMIZAÇÃO
# ==========================================
#
# Este Dockerfile usa multi-stage build para:
# 1. Reduzir tamanho da imagem final
# 2. Separar dependências de build das de runtime
# 3. Melhorar segurança usando usuário não-root
# 4. Otimizar cache de layers do Docker
#
# Tamanho aproximado da imagem: ~200MB
#
# ==========================================
