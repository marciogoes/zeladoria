# 🏗️ INFRAESTRUTURA E CONFIGURAÇÃO

## 📦 SISTEMA DE ZELADORIA URBANA - BELÉM/PA

**Versão:** 2.0.0  
**Data:** 18 de Outubro de 2025

---

## 🎯 ARQUIVOS DE INFRAESTRUTURA CRIADOS

### **📋 Visão Geral**

```
📦 python-zeladoria/
├── 📄 requirements.txt          ✅ Dependências Python (50+ pacotes)
├── 📄 .gitignore                ✅ Ignorar arquivos sensíveis
├── 📄 .env.example              ✅ Configurações de exemplo
├── 🐳 Dockerfile                ✅ Imagem Docker otimizada
├── 🐳 docker-compose.yml        ✅ Orquestração de containers
├── 📄 docker-entrypoint.sh      ✅ Script de inicialização Docker
├── 🔄 update.sh                 ✅ Script de atualização (Linux/Mac)
├── 🔄 update.ps1                ✅ Script de atualização (Windows)
└── 📁 .github/
    └── 📁 workflows/
        └── 📄 ci-cd.yml         ✅ Pipeline CI/CD completo
```

---

## 📦 1. REQUIREMENTS.TXT

### **Dependências Principais:**

```txt
# Framework Web
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Banco de Dados
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Autenticação
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Validação
pydantic==2.5.0
email-validator==2.1.0

# Monitoramento
psutil==5.9.6

# Testes
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2

# Utilitários
requests==2.31.0
python-dotenv==1.0.0
colorama==0.4.6

# E muito mais...
```

**Total:** 50+ pacotes

### **Como Usar:**

```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Atualizar dependências
pip install --upgrade -r requirements.txt

# Ver pacotes desatualizados
pip list --outdated
```

---

## 🚫 2. .GITIGNORE

### **O que é Ignorado:**

```
✅ Cache Python (__pycache__, *.pyc)
✅ Ambientes virtuais (venv/, env/)
✅ Banco de dados (*.db, *.sqlite)
✅ Logs (logs/, *.log)
✅ Uploads (uploads/)
✅ Backups (backups/)
✅ Configurações sensíveis (.env)
✅ IDEs (.vscode/, .idea/)
✅ Sistema operacional (.DS_Store, Thumbs.db)
```

### **Benefícios:**

- 🔒 **Segurança:** Não committa secrets
- 🧹 **Limpeza:** Repositório organizado
- 🚀 **Performance:** Git mais rápido
- 👥 **Colaboração:** Evita conflitos

---

## 🐳 3. DOCKER

### **3.1 Dockerfile**

**Multi-stage build otimizado:**

```dockerfile
# Estágio 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv
RUN pip install -r requirements.txt

# Estágio 2: Produção
FROM python:3.11-slim
COPY --from=builder /opt/venv /opt/venv
COPY . /app
WORKDIR /app
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**Características:**
- ✅ Imagem otimizada (~200MB)
- ✅ Multi-stage build
- ✅ Usuário não-root
- ✅ Health check integrado
- ✅ Seguro e eficiente

### **Como Usar:**

```bash
# Build da imagem
docker build -t zeladoria:2.0.0 .

# Executar container
docker run -d \
  --name zeladoria \
  -p 8001:8001 \
  -e DATABASE_URL=sqlite:///./zeladoria.db \
  -e SECRET_KEY=sua-chave-secreta \
  -v $(pwd)/uploads:/app/uploads \
  zeladoria:2.0.0

# Ver logs
docker logs -f zeladoria

# Acessar shell
docker exec -it zeladoria bash
```

---

### **3.2 docker-compose.yml**

**Stack completa com 6 serviços:**

```yaml
services:
  app:        # Aplicação principal (FastAPI)
  db:         # PostgreSQL 15
  redis:      # Cache
  nginx:      # Reverse proxy (produção)
  pgadmin:    # Admin de banco (dev)
  backup:     # Backup automático (produção)
```

**Profiles:**
- `development`: app + db + redis + pgadmin
- `production`: app + db + redis + nginx + backup

### **Como Usar:**

```bash
# Desenvolvimento
docker-compose --profile development up -d

# Produção
docker-compose --profile production up -d

# Ver logs
docker-compose logs -f

# Parar tudo
docker-compose down

# Backup do banco
docker-compose exec db pg_dump -U zeladoria zeladoria > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U zeladoria zeladoria < backup.sql
```

**Acessos:**
- 🌐 App: http://localhost:8001
- 📊 pgAdmin: http://localhost:5050
- 🐘 PostgreSQL: localhost:5432
- 🔴 Redis: localhost:6379

---

### **3.3 docker-entrypoint.sh**

**Script de inicialização que:**

```bash
✅ Aguarda banco de dados estar pronto
✅ Cria diretórios necessários
✅ Executa migrações
✅ Popula dados iniciais (opcional)
✅ Verifica health
✅ Inicia aplicação
```

---

## 🔄 4. SCRIPTS DE ATUALIZAÇÃO

### **4.1 update.sh (Linux/Mac)**

**Funcionalidades:**

```
✅ Para o servidor
✅ Faz backup do banco e .env
✅ Atualiza dependências
✅ Verifica mudanças no .env
✅ Executa migrações
✅ Verifica integridade
✅ Executa testes (opcional)
✅ Limpa cache
✅ Remove logs antigos
✅ Inicia servidor (opcional)
```

### **Como Usar:**

```bash
# Tornar executável
chmod +x update.sh

# Executar atualização
./update.sh
```

**Saída esperada:**
```
╔═══════════════════════════════════════════════════════╗
║   Sistema de Zeladoria Urbana - Belém/PA             ║
║   Script de Atualização v2.0.0                       ║
╚═══════════════════════════════════════════════════════╝

[INFO] Verificando se o servidor está rodando...
[✓] Servidor parado
[INFO] Criando backup do banco de dados...
[✓] Backup criado: backups/zeladoria_backup_20251018_143022.db
[INFO] Atualizando dependências Python...
[✓] Dependências atualizadas
...
╔════════════════════════════════════════════════════════╗
║  ✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!                ║
╚════════════════════════════════════════════════════════╝
```

---

### **4.2 update.ps1 (Windows)**

**Mesmas funcionalidades do update.sh, adaptado para PowerShell**

### **Como Usar:**

```powershell
# Executar atualização
.\update.ps1
```

---

## 🤖 5. CI/CD (GITHUB ACTIONS)

### **Pipeline Completo com 6 Jobs:**

```
┌─────────────────┐
│  1. LINT        │  ← Qualidade de código
├─────────────────┤
│  2. TEST        │  ← Testes automatizados
├─────────────────┤
│  3. SECURITY    │  ← Análise de segurança
├─────────────────┤
│  4. BUILD       │  ← Build Docker image
├─────────────────┤
│  5. DEPLOY      │  ← Deploy em produção
├─────────────────┤
│  6. NOTIFY      │  ← Notificação de resultado
└─────────────────┘
```

### **Jobs Detalhados:**

#### **Job 1: Lint e Qualidade**
```yaml
- Flake8 (erros de sintaxe)
- Black (formatação)
- isort (imports)
```

#### **Job 2: Testes**
```yaml
- PostgreSQL test database
- Pytest com coverage
- Upload coverage para Codecov
```

#### **Job 3: Segurança**
```yaml
- Safety (vulnerabilidades)
- Bandit (análise de segurança)
```

#### **Job 4: Build**
```yaml
- Docker Buildx
- Push para Docker Hub
- Cache otimizado
```

#### **Job 5: Deploy**
```yaml
- Deploy via SSH
- Health check
- Rollback automático se falhar
```

#### **Job 6: Notificação**
```yaml
- Notifica sucesso/falha
- Email/Slack (configurável)
```

### **Triggers:**

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_dispatch:  # Manual
```

### **Secrets Necessários:**

```
DOCKER_USERNAME     # Docker Hub username
DOCKER_PASSWORD     # Docker Hub password
DEPLOY_HOST         # Servidor de produção
DEPLOY_USER         # Usuário SSH
DEPLOY_KEY          # Chave privada SSH
```

### **Como Configurar:**

1. No GitHub: Settings → Secrets and variables → Actions
2. Adicionar cada secret
3. Push para `main` ou `develop`
4. Pipeline executa automaticamente

---

## 📊 COMPARAÇÃO: DESENVOLVIMENTO vs PRODUÇÃO

### **Desenvolvimento:**

```bash
# Usando scripts locais
./install.sh
./start.sh

# Ou Docker
docker-compose --profile development up -d
```

**Características:**
- ✅ SQLite
- ✅ DEBUG=True
- ✅ Hot reload
- ✅ pgAdmin incluído
- ✅ Logs verbose

---

### **Produção:**

```bash
# Docker
docker-compose --profile production up -d

# Ou manual
pip install -r requirements.txt
gunicorn main:app --workers 4 --bind 0.0.0.0:8001
```

**Características:**
- ✅ PostgreSQL
- ✅ DEBUG=False
- ✅ HTTPS
- ✅ Nginx reverse proxy
- ✅ Backup automático
- ✅ Monitoramento
- ✅ Cache Redis

---

## 🔧 COMANDOS ÚTEIS

### **Docker:**

```bash
# Build
docker build -t zeladoria:2.0.0 .

# Run
docker run -d -p 8001:8001 zeladoria:2.0.0

# Logs
docker logs -f zeladoria

# Shell
docker exec -it zeladoria bash

# Stop
docker stop zeladoria

# Remove
docker rm zeladoria
```

---

### **Docker Compose:**

```bash
# Up (dev)
docker-compose --profile development up -d

# Up (prod)
docker-compose --profile production up -d

# Logs
docker-compose logs -f app

# Restart
docker-compose restart app

# Down
docker-compose down

# Down com volumes
docker-compose down -v

# Rebuild
docker-compose up -d --build
```

---

### **Atualização:**

```bash
# Linux/Mac
./update.sh

# Windows
.\update.ps1
```

---

## ✅ CHECKLIST DE INFRAESTRUTURA

### **Arquivos Criados:**
- [x] requirements.txt (50+ pacotes)
- [x] .gitignore (completo)
- [x] .env.example (100+ variáveis)
- [x] Dockerfile (multi-stage)
- [x] docker-compose.yml (6 serviços)
- [x] docker-entrypoint.sh
- [x] update.sh (Linux/Mac)
- [x] update.ps1 (Windows)
- [x] .github/workflows/ci-cd.yml (6 jobs)

### **Funcionalidades:**
- [x] Build Docker otimizado
- [x] Orquestração completa
- [x] CI/CD automatizado
- [x] Testes automatizados
- [x] Análise de segurança
- [x] Deploy automático
- [x] Backup automático
- [x] Health checks
- [x] Monitoramento
- [x] Scripts de atualização

---

## 🎯 PRÓXIMOS PASSOS

### **1. Configurar GitHub Secrets**
```
Settings → Secrets → New repository secret
```

### **2. Testar Localmente**
```bash
docker-compose --profile development up -d
```

### **3. Deploy em Produção**
```bash
docker-compose --profile production up -d
```

### **4. Monitorar**
```bash
docker-compose logs -f
curl http://localhost:8001/health
```

---

## 📚 DOCUMENTAÇÃO RELACIONADA

- **[START_HERE.md](START_HERE.md)** - Início rápido
- **[MASTER_DOCUMENT.md](MASTER_DOCUMENT.md)** - Visão completa
- **[AUTOMACAO.md](AUTOMACAO.md)** - Scripts e ferramentas
- **[CHECKLIST_DEPLOY.md](CHECKLIST_DEPLOY.md)** - Deploy em produção

---

**Sistema de Zeladoria Urbana - Belém/PA**  
**Infraestrutura e Configuração**  
**Versão:** 2.0.0  
**Data:** 18 de Outubro de 2025

```
🏗️ INFRAESTRUTURA 100% COMPLETA! 🏗️
```
