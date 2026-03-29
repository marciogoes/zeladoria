# 🔧 FERRAMENTAS DE AUTOMAÇÃO E SCRIPTS

## 📦 SISTEMA DE ZELADORIA URBANA - BELÉM/PA

**Versão:** 2.0.0  
**Data:** 18 de Outubro de 2025

---

## 🎯 FERRAMENTAS DISPONÍVEIS

### **1. Scripts de Instalação** 🚀

#### **Linux/Mac: `install.sh`**
```bash
./install.sh
```

**O que faz:**
- ✅ Verifica Python e pip
- ✅ Cria ambiente virtual
- ✅ Instala dependências
- ✅ Cria diretórios necessários
- ✅ Configura .env
- ✅ Inicializa banco de dados
- ✅ Popula dados de teste (opcional)
- ✅ Cria scripts auxiliares
- ✅ Configura backup automático (opcional)
- ✅ Executa testes básicos

**Tempo estimado:** 2-5 minutos

---

#### **Windows: `install.ps1`**
```powershell
.\install.ps1
```

**O que faz:**
- ✅ Mesmas funcionalidades do install.sh
- ✅ Adaptado para PowerShell
- ✅ Compatível com Windows 10/11

**Nota:** Execute com PowerShell como Administrador

---

### **2. Scripts de Gerenciamento** ⚙️

#### **Iniciar Sistema**

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```powershell
.\start.ps1
```

**O que faz:**
- ✅ Ativa ambiente virtual
- ✅ Inicia backend (porta 8001)
- ✅ Exibe informações de acesso
- ✅ Mantém servidor rodando

**Saída esperada:**
```
🚀 Iniciando Sistema de Zeladoria Urbana...
📡 Iniciando backend na porta 8001...
✅ Backend iniciado

╔════════════════════════════════════════════════╗
║  Sistema de Zeladoria Urbana - Pronto!        ║
╠════════════════════════════════════════════════╣
║  🌐 Frontend: http://localhost:8001/static/   ║
║  📡 API: http://localhost:8001/api            ║
║  📚 Docs: http://localhost:8001/docs          ║
║  👤 Login: maria.santos@belem.pa.gov.br       ║
╚════════════════════════════════════════════════╝
```

---

#### **Parar Sistema**

**Linux/Mac:**
```bash
./stop.sh
```

**Windows:**
```powershell
.\stop.ps1
```

**O que faz:**
- ✅ Encontra processo do uvicorn
- ✅ Encerra o servidor
- ✅ Confirma parada

---

#### **Fazer Backup**

**Linux/Mac:**
```bash
./backup.sh
```

**Windows:**
```powershell
.\backup.ps1
```

**O que faz:**
- ✅ Cria backup compactado (.tar.gz ou .zip)
- ✅ Inclui: banco de dados, .env, uploads, logs
- ✅ Nome com timestamp
- ✅ Mantém últimos 7 backups
- ✅ Remove backups antigos automaticamente

**Saída:**
```
💾 Criando backup...
✅ Backup criado: backups/zeladoria_backup_20251018_143022.tar.gz
🗑️  Backups antigos removidos (mantidos últimos 7)
```

---

### **3. Suite de Testes** 🧪

#### **Executar Testes Automatizados**

```bash
python test_suite.py
```

**O que testa:**

**Infraestrutura:**
- ✅ Backend Health Check
- ✅ API Docs acessível
- ✅ Frontend acessível
- ✅ Conexão com banco de dados
- ✅ Tempo de resposta

**Autenticação:**
- ✅ Login funcional
- ✅ Token JWT válido

**Endpoints:**
- ✅ Listar categorias
- ✅ Listar bairros
- ✅ Listar chamados
- ✅ Dashboard

**Configuração:**
- ✅ CORS configurado
- ✅ Arquivos estáticos
  - app.js
  - dashboard.js
  - dashboard-advanced.js

**Saída esperada:**
```
════════════════════════════════════════════════════════════
            SUITE DE TESTES AUTOMATIZADOS
════════════════════════════════════════════════════════════

[TEST] Backend Health Check... ✓ OK
[TEST] API Docs (/docs)... ✓ OK
[TEST] Frontend (index.html)... ✓ OK
[TEST] Auth - Login... ✓ OK
...

════════════════════════════════════════════════════════════
                    RESUMO DOS TESTES
════════════════════════════════════════════════════════════

Total de testes: 15
✓ Passaram: 15
✗ Falharam: 0
⊘ Pulados: 0

           🎉 TODOS OS TESTES PASSARAM! 🎉
```

---

### **4. Health Check API** 💊

#### **Endpoints Disponíveis:**

**1. Health Check Básico**
```bash
GET /health
```

**Resposta:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-18T14:30:22",
  "service": "Sistema de Zeladoria Urbana - Belém/PA",
  "version": "2.0.0"
}
```

---

**2. Health Check Detalhado**
```bash
GET /health/detailed
```

**Resposta:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-18T14:30:22",
  "service": "Sistema de Zeladoria Urbana - Belém/PA",
  "version": "2.0.0",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Conexão OK"
    },
    "cpu": {
      "status": "healthy",
      "usage_percent": 45.2,
      "cores": 8
    },
    "memory": {
      "status": "healthy",
      "usage_percent": 62.5,
      "available_mb": 4096,
      "total_mb": 16384
    },
    "disk": {
      "status": "healthy",
      "usage_percent": 35.8,
      "available_gb": 450,
      "total_gb": 500
    }
  }
}
```

---

**3. Readiness Check** (Kubernetes)
```bash
GET /health/readiness
```

**Resposta:**
- 200 OK se pronto
- 503 Service Unavailable se não pronto

---

**4. Liveness Check** (Kubernetes)
```bash
GET /health/liveness
```

**Resposta:**
- 200 OK se vivo

---

**5. Métricas** (Prometheus)
```bash
GET /metrics
```

**Resposta:**
```json
{
  "timestamp": "2025-10-18T14:30:22",
  "application": {
    "name": "zeladoria_urbana",
    "version": "2.0.0",
    "uptime_seconds": 3600
  },
  "system": {
    "cpu_usage_percent": 45.2,
    "memory_usage_percent": 62.5,
    "disk_usage_percent": 35.8
  },
  "database": {
    "status": "healthy",
    "tables": {
      "chamados": 120,
      "usuarios": 25,
      "categorias": 12
    }
  }
}
```

---

### **5. Configuração (.env.example)** ⚙️

**Arquivo completo de configuração com mais de 100 variáveis:**

```env
# Principais seções:
- Banco de Dados (SQLite, PostgreSQL, MySQL)
- Segurança (JWT, SECRET_KEY)
- API (URLs, CORS)
- Uploads (tamanhos, extensões)
- Email (SMTP)
- Logs (níveis, rotação)
- Geolocalização (coordenadas padrão)
- SLA (tempos por prioridade)
- Cache (Redis, memory)
- Backup (retenção, schedule)
- Dashboard (refresh, períodos)
- Features Flags (habilitar/desabilitar)
- E muito mais...
```

---

## 📋 FLUXO DE USO

### **Primeira Instalação:**

```bash
# 1. Clonar/baixar o projeto
cd python-zeladoria

# 2. Executar instalação (Linux/Mac)
chmod +x install.sh
./install.sh

# Ou Windows
.\install.ps1

# 3. Aguardar instalação (2-5 min)
# 4. Revisar .env se necessário

# 5. Iniciar sistema
./start.sh  # ou .\start.ps1

# 6. Acessar
# http://localhost:8001/static/index.html
```

---

### **Uso Diário:**

```bash
# Iniciar
./start.sh

# Parar
./stop.sh

# Backup manual
./backup.sh

# Executar testes
python test_suite.py

# Ver health
curl http://localhost:8001/health
```

---

### **Monitoramento:**

```bash
# Health check básico
curl http://localhost:8001/health

# Health check detalhado
curl http://localhost:8001/health/detailed

# Métricas
curl http://localhost:8001/metrics

# Logs em tempo real
tail -f logs/app.log
```

---

## 🔄 AUTOMAÇÃO DE BACKUPS

### **Configurar Backup Automático (Linux/Mac):**

Durante a instalação, você pode optar por configurar backup automático diário.

**Ou configure manualmente:**

```bash
# Adicionar ao crontab
crontab -e

# Adicionar linha:
0 2 * * * cd /caminho/para/zeladoria && ./backup.sh >> logs/backup.log 2>&1
```

**Isso executará backup todos os dias às 2h da manhã.**

---

### **Configurar Backup Automático (Windows):**

**Agendador de Tarefas:**

1. Abrir "Agendador de Tarefas"
2. Criar Nova Tarefa
3. Nome: "Backup Zeladoria"
4. Gatilho: Diariamente às 2:00
5. Ação: Executar programa
   - Programa: `powershell.exe`
   - Argumentos: `-File "C:\caminho\para\backup.ps1"`
6. Salvar

---

## 🐛 TROUBLESHOOTING

### **Problema: install.sh não executa**

**Solução:**
```bash
chmod +x install.sh
./install.sh
```

---

### **Problema: PowerShell bloqueia execução**

**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

---

### **Problema: Testes falham**

**Causas comuns:**
1. Backend não está rodando
2. Banco de dados vazio
3. Porta 8001 ocupada

**Solução:**
```bash
# 1. Iniciar backend
./start.sh

# 2. Popular banco
python seed.py

# 3. Verificar porta
lsof -i :8001  # Linux/Mac
netstat -ano | findstr :8001  # Windows

# 4. Executar testes novamente
python test_suite.py
```

---

### **Problema: Health check falha**

**Verificar:**
```bash
# 1. Backend rodando?
curl http://localhost:8001/health

# 2. Banco de dados OK?
python -c "from app.database import engine; engine.connect()"

# 3. Logs
tail -f logs/app.log
```

---

## 📊 MÉTRICAS E MONITORAMENTO

### **Integração com Monitoramento Externo:**

#### **Prometheus:**
```yaml
scrape_configs:
  - job_name: 'zeladoria'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
```

#### **Grafana Dashboard:**
- CPU Usage
- Memory Usage
- Disk Usage
- Request Rate
- Response Time
- Database Connections
- Total Chamados
- Active Users

#### **Alertmanager:**
```yaml
route:
  receiver: 'email'
  
receivers:
  - name: 'email'
    email_configs:
      - to: 'admin@zeladoria-belem.gov.br'
        from: 'alertas@zeladoria-belem.gov.br'
        
rules:
  - alert: HighCPUUsage
    expr: cpu_usage_percent > 80
    for: 5m
    annotations:
      summary: "CPU usage alto"
```

---

## 🎯 BOAS PRÁTICAS

### **1. Executar testes antes de deploy**
```bash
python test_suite.py
```

### **2. Fazer backup antes de atualizações**
```bash
./backup.sh
```

### **3. Monitorar health checks**
```bash
# Adicionar ao monitoring
watch -n 60 'curl -s http://localhost:8001/health | jq .'
```

### **4. Revisar logs regularmente**
```bash
tail -f logs/app.log
```

### **5. Manter .env atualizado**
```bash
# Usar .env.example como referência
diff .env .env.example
```

---

## ✅ CHECKLIST DE MANUTENÇÃO

### **Diário:**
- [ ] Verificar health check
- [ ] Revisar logs de erro
- [ ] Monitorar métricas

### **Semanal:**
- [ ] Executar suite de testes
- [ ] Verificar backups
- [ ] Limpar logs antigos
- [ ] Atualizar dependências (se necessário)

### **Mensal:**
- [ ] Backup completo manual
- [ ] Análise de performance
- [ ] Revisão de segurança
- [ ] Atualização de documentação

---

## 📚 RECURSOS ADICIONAIS

### **Documentação:**
- [INDEX.md](INDEX.md) - Índice completo
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Referência rápida
- [CHECKLIST_DEPLOY.md](CHECKLIST_DEPLOY.md) - Deploy em produção

### **Ferramentas Externas:**
- **Postman:** Testar API manualmente
- **pgAdmin:** Gerenciar PostgreSQL
- **Sentry:** Rastreamento de erros
- **New Relic:** APM e monitoramento
- **Grafana:** Visualização de métricas

---

## 🎉 CONCLUSÃO

Com essas ferramentas de automação, você tem:

✅ **Instalação automatizada** (2-5 min)  
✅ **Scripts de gerenciamento** (start, stop, backup)  
✅ **Suite de testes** (15+ testes)  
✅ **Health checks** (5 endpoints)  
✅ **Configuração completa** (100+ variáveis)  
✅ **Monitoramento** (métricas, logs)  
✅ **Backup automático** (diário)  
✅ **Troubleshooting** (guia completo)  

---

**Sistema de Zeladoria Urbana - Belém/PA**  
**Ferramentas de Automação e Scripts**  
**Versão:** 2.0.0  
**Data:** 18 de Outubro de 2025

```
🔧 FERRAMENTAS PRONTAS PARA USO! 🔧
```
