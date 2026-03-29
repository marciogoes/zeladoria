# 🦇 GUIA DOS ARQUIVOS .BAT

## 📦 SISTEMA DE ZELADORIA URBANA - BELÉM/PA

**Versão:** 2.0.0  
**Data:** 18 de Outubro de 2025

---

## 🎯 ARQUIVOS .BAT DISPONÍVEIS

```
📁 python-zeladoria/
├── 🦇 install.bat        ⭐ Instalação automatizada
├── 🦇 update.bat         Atualização do sistema
├── 🦇 start.bat          Iniciar sistema (criado pelo install.bat)
├── 🦇 stop.bat           Parar sistema (criado pelo install.bat)
└── 🦇 backup.bat         Backup manual (criado pelo install.bat)
```

---

## 🚀 COMO USAR

### **1️⃣ INSTALAÇÃO (install.bat)**

**Primeira vez usando o sistema:**

```batch
# Clique duas vezes em install.bat
# OU execute no Prompt de Comando:
install.bat
```

**O que o script faz:**

```
✅ Verifica Python e pip
✅ Cria ambiente virtual
✅ Instala todas as dependências
✅ Cria diretórios (uploads, logs, backups)
✅ Configura .env automaticamente
✅ Inicializa banco de dados
✅ Popula dados de teste (opcional)
✅ Verifica Node.js (opcional)
✅ Cria scripts auxiliares (start, stop, backup)
✅ Executa testes básicos
✅ Oferece iniciar o servidor
```

**Tempo estimado:** 2-5 minutos

**Saída esperada:**
```
╔═══════════════════════════════════════════════════════╗
║   Sistema de Zeladoria Urbana - Belém/PA             ║
║   Instalação Automatizada v2.0.0                     ║
╚═══════════════════════════════════════════════════════╝

[INFO] Verificando Python...
[√] Python 3.11.5 encontrado
[INFO] Criando ambiente virtual...
[√] Ambiente virtual criado
...
╔════════════════════════════════════════════════════════╗
║  ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!                 ║
╚════════════════════════════════════════════════════════╝
```

---

### **2️⃣ INICIAR SISTEMA (start.bat)**

**Iniciar o servidor:**

```batch
# Clique duas vezes em start.bat
# OU execute no Prompt de Comando:
start.bat
```

**O que acontece:**

```
✅ Ativa ambiente virtual
✅ Inicia backend na porta 8001
✅ Mostra informações de acesso
✅ Mantém servidor rodando
```

**Saída esperada:**
```
🚀 Iniciando Sistema de Zeladoria Urbana...
📡 Iniciando backend na porta 8001...

╔════════════════════════════════════════════════╗
║  Sistema de Zeladoria Urbana - Pronto!        ║
╠════════════════════════════════════════════════╣
║                                                ║
║  🌐 Frontend: http://localhost:8001/static/   ║
║  📡 API: http://localhost:8001/api            ║
║  📚 Docs: http://localhost:8001/docs          ║
║                                                ║
║  👤 Login de Teste (Gestor):                  ║
║  Email: maria.santos@belem.pa.gov.br          ║
║  Senha: senha123                              ║
║                                                ║
╚════════════════════════════════════════════════╝

Pressione Ctrl+C para parar o servidor
```

---

### **3️⃣ PARAR SISTEMA (stop.bat)**

**Parar o servidor:**

```batch
# Clique duas vezes em stop.bat
# OU execute no Prompt de Comando:
stop.bat
```

**O que acontece:**

```
✅ Encontra processos Python (uvicorn)
✅ Para todos os processos
✅ Confirma parada
```

**Saída esperada:**
```
🛑 Parando Sistema de Zeladoria Urbana...
✅ Backend parado
```

---

### **4️⃣ FAZER BACKUP (backup.bat)**

**Criar backup manual:**

```batch
# Clique duas vezes em backup.bat
# OU execute no Prompt de Comando:
backup.bat
```

**O que o script faz:**

```
✅ Cria backup compactado (.zip)
✅ Inclui: banco de dados, .env, uploads, logs
✅ Nome com timestamp
✅ Mantém últimos 7 backups
✅ Remove backups antigos automaticamente
```

**Saída esperada:**
```
💾 Criando backup...
✅ Backup criado: backups\zeladoria_backup_20251018_143022.zip
🗑️  Backups antigos removidos (mantidos últimos 7)
```

---

### **5️⃣ ATUALIZAR SISTEMA (update.bat)**

**Atualizar o sistema:**

```batch
# Clique duas vezes em update.bat
# OU execute no Prompt de Comando:
update.bat
```

**O que o script faz:**

```
✅ Para o servidor
✅ Faz backup do banco e .env
✅ Atualiza dependências
✅ Verifica mudanças no .env
✅ Executa migrações
✅ Verifica integridade
✅ Executa testes (opcional)
✅ Limpa cache Python
✅ Remove logs antigos
✅ Oferece iniciar servidor
```

**Saída esperada:**
```
╔═══════════════════════════════════════════════════════╗
║   Sistema de Zeladoria Urbana - Belém/PA             ║
║   Script de Atualização v2.0.0                       ║
╚═══════════════════════════════════════════════════════╝

[INFO] Verificando se o servidor está rodando...
[√] Servidor parado
[INFO] Criando backup do banco de dados...
[√] Backup criado
...
╔════════════════════════════════════════════════════════╗
║  ✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!                ║
╚════════════════════════════════════════════════════════╝
```

---

## 🎯 FLUXO DE USO DIÁRIO

### **Primeira Vez:**
```
1. install.bat    (executar UMA VEZ)
   ↓
2. start.bat      (iniciar sistema)
   ↓
3. Acessar no navegador
```

### **Uso Diário:**
```
1. start.bat      (iniciar)
   ↓
2. Trabalhar no sistema
   ↓
3. stop.bat       (parar)
```

### **Backup:**
```
backup.bat        (quando necessário)
```

### **Atualização:**
```
update.bat        (quando houver atualizações)
```

---

## ⚠️ PROBLEMAS COMUNS

### **Problema 1: "Python não encontrado"**

**Causa:** Python não está instalado ou não está no PATH

**Solução:**
```
1. Baixe Python: https://www.python.org/downloads/
2. Durante a instalação, marque "Add Python to PATH"
3. Reinicie o Prompt de Comando
4. Execute install.bat novamente
```

---

### **Problema 2: "Erro ao ativar ambiente virtual"**

**Causa:** Ambiente virtual corrompido

**Solução:**
```batch
# Remova o diretório venv
rd /s /q venv

# Execute install.bat novamente
install.bat
```

---

### **Problema 3: "Porta 8001 já está em uso"**

**Causa:** Outro processo usando a porta

**Solução:**
```batch
# Execute stop.bat para parar processos antigos
stop.bat

# Ou encontre e mate o processo manualmente:
netstat -ano | findstr :8001
taskkill /PID [número_do_pid] /F

# Inicie novamente
start.bat
```

---

### **Problema 4: "Módulo não encontrado"**

**Causa:** Dependências não instaladas

**Solução:**
```batch
# Ative o ambiente virtual
venv\Scripts\activate.bat

# Instale as dependências manualmente
pip install -r requirements.txt

# Ou execute install.bat novamente
install.bat
```

---

### **Problema 5: "Banco de dados corrompido"**

**Causa:** Banco de dados com problemas

**Solução:**
```batch
# 1. Faça backup (se possível)
backup.bat

# 2. Remova o banco atual
del zeladoria.db

# 3. Recrie o banco
venv\Scripts\activate.bat
python -c "from app.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"

# 4. Popule dados de teste
python seed.py
```

---

## 📋 CHECKLIST DE VERIFICAÇÃO

### **Antes de executar install.bat:**
- [ ] Python 3.8+ instalado
- [ ] Python no PATH do sistema
- [ ] Espaço em disco (mínimo 500MB)
- [ ] Conexão com internet (para baixar dependências)

### **Após executar install.bat:**
- [ ] Diretórios criados (uploads, logs, backups)
- [ ] Arquivo .env criado
- [ ] Banco de dados criado (zeladoria.db)
- [ ] Scripts auxiliares criados (start, stop, backup)

### **Para usar diariamente:**
- [ ] start.bat funciona sem erros
- [ ] Sistema acessível em localhost:8001
- [ ] Login funciona corretamente
- [ ] Dashboard carrega completamente

---

## 💡 DICAS

### **Dica 1: Executar no Prompt de Comando**
```batch
# Abra o Prompt de Comando no diretório do projeto
cd C:\caminho\para\python-zeladoria

# Execute o script desejado
install.bat
```

### **Dica 2: Ver Logs em Tempo Real**
```batch
# Após iniciar o sistema com start.bat
# Abra outro Prompt de Comando e execute:
type logs\app.log
```

### **Dica 3: Verificar Status**
```batch
# Ver se o servidor está rodando:
tasklist | findstr python

# Ver qual processo está na porta 8001:
netstat -ano | findstr :8001
```

### **Dica 4: Backup Automático**
```batch
# Agende backup diário usando Agendador de Tarefas
# 1. Abra "Agendador de Tarefas"
# 2. Criar Tarefa Básica
# 3. Nome: "Backup Zeladoria"
# 4. Gatilho: Diário às 2:00
# 5. Ação: Iniciar programa
# 6. Programa: cmd.exe
# 7. Argumentos: /c "C:\caminho\backup.bat"
```

---

## 🔧 COMANDOS ÚTEIS

### **Gerenciamento do Sistema:**
```batch
# Instalar pela primeira vez
install.bat

# Iniciar servidor
start.bat

# Parar servidor
stop.bat

# Fazer backup
backup.bat

# Atualizar sistema
update.bat
```

### **Comandos Manuais (se necessário):**
```batch
# Ativar ambiente virtual
venv\Scripts\activate.bat

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor manualmente
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Executar testes
python test_suite.py

# Popular banco de dados
python seed.py
```

---

## 📚 DOCUMENTAÇÃO RELACIONADA

- **[START_HERE.md](START_HERE.md)** - Início rápido
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Referência rápida
- **[AUTOMACAO.md](AUTOMACAO.md)** - Scripts e ferramentas
- **[INFRAESTRUTURA.md](INFRAESTRUTURA.md)** - Configuração completa

---

## ✅ RESUMO

```
📦 INSTALAÇÃO
   install.bat          Uma vez, no início

📅 USO DIÁRIO
   start.bat            Para iniciar
   stop.bat             Para parar

💾 MANUTENÇÃO
   backup.bat           Backups manuais
   update.bat           Atualizações

⏱️  TEMPO
   Instalação: 2-5 min
   Start/Stop: <30 seg
   Backup: <1 min
   Update: 2-3 min
```

---

**Sistema de Zeladoria Urbana - Belém/PA**  
**Guia dos Arquivos .BAT**  
**Versão:** 2.0.0  
**Data:** 18 de Outubro de 2025

```
🦇 ARQUIVOS .BAT PRONTOS PARA USO! 🦇

  install.bat  →  Instalação automática
  start.bat    →  Iniciar sistema
  stop.bat     →  Parar sistema
  backup.bat   →  Fazer backup
  update.bat   →  Atualizar sistema

    FÁCIL, RÁPIDO E AUTOMATIZADO!
```
