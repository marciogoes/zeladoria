# ⚡ INÍCIO RÁPIDO - SISTEMA DE SECRETARIAS

## 🚀 COMECE EM 3 MINUTOS

---

## 📦 VERSÃO 2.1 - SECRETARIAS MUNICIPAIS

Agora com **15 secretarias reais** da Prefeitura de Belém!

---

## 🎯 ESCOLHA SUA OPÇÃO

### **OPÇÃO 1: INSTALAÇÃO NOVA** (Recomendado)

```batch
REM 1. Remover banco antigo
del zeladoria.db

REM 2. Criar novo com secretarias
venv\Scripts\activate.bat
python seed.py

REM 3. Reiniciar
stop.bat
start.bat

REM 4. Testar
REM http://localhost:8001/static/index.html
```

**Tempo:** 2 minutos

---

### **OPÇÃO 2: MIGRAR BANCO EXISTENTE**

```batch
REM 1. Executar migração
migrar.bat

REM 2. Seguir instruções
REM (Backup automático)

REM 3. Reiniciar
stop.bat
start.bat
```

**Tempo:** 3 minutos

---

## 👤 LOGINS DE TESTE

### **Secretaria (vê apenas seus chamados):**
```
SEURB (Urbanismo):
Email: carlos.mendes@seurb.belem.pa.gov.br
Senha: senha123
```

### **Gestor (vê tudo):**
```
Email: maria.santos@belem.pa.gov.br
Senha: senha123
```

---

## 🎯 O QUE TESTAR

1. **Login como Secretaria (SEURB)**
   - Veja apenas 4 categorias de urbanismo
   - Dashboard específico da SEURB

2. **Login como Gestor**
   - Veja TODAS as categorias
   - Dashboard consolidado

3. **Compare os dashboards**
   - Secretaria: visão focada
   - Gestor: visão geral

---

## 🏛️ SECRETARIAS DISPONÍVEIS

```
✅ SEURB - Urbanismo (Buraco, Iluminação, Calçada, Sinalização)
✅ SESAN - Saneamento (Lixo, Esgoto, Coleta)
✅ SEMMA - Meio Ambiente (Poda, Área verde, Animal)
✅ SESMA - Saúde (Dengue)
✅ SEJEL - Esporte (Equipamentos)
✅ GMB - Segurança
✅ SEMEC - Educação
✅ SEHAB - Habitação
... e mais 7 secretarias
```

---

## 📋 DIFERENÇAS PRINCIPAIS

### **PERFIL SECRETARIA:**
- Vê APENAS seus chamados
- Dashboard específico
- 4-5 categorias

### **PERFIL GESTOR:**
- Vê TODOS os chamados
- Dashboard geral
- Todas as categorias

---

## ❓ PROBLEMAS?

**Erro na migração?**
```batch
REM Restaurar backup
copy backups\zeladoria_backup_*.db zeladoria.db
```

**Banco não atualiza?**
```batch
REM Forçar recriação
del zeladoria.db
python seed.py
```

---

## 📚 MAIS INFORMAÇÕES

- **SECRETARIAS.md** - Guia completo
- **ATUALIZACAO_V2.1.md** - O que mudou
- **MASTER_DOCUMENT.md** - Visão geral

---

## ✅ PRONTO!

```
🏛️ 15 SECRETARIAS
👥 7 USUÁRIOS DE TESTE
🔗 CATEGORIAS ASSOCIADAS
⚡ PRONTO EM 3 MINUTOS!
```

**Acesse agora:**
http://localhost:8001/static/index.html

---

Sistema de Zeladoria Urbana - Belém/PA
Versão 2.1.0 - Sistema de Secretarias
