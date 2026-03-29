# 🏛️ Sistema de Zeladoria Urbana - Belém/PA
## Versão 2.0 - Com Catálogo de Serviços e Secretarias

---

## 🚀 INÍCIO RÁPIDO

### 1️⃣ **Setup Completo (Execute UMA VEZ):**

```
SETUP_COMPLETO.bat
```

Isso vai:
- ✅ Criar tabelas no banco
- ✅ Criar 5 secretarias (SEURB, SESAN, SEMOB, SEMMA, SESMA)
- ✅ Criar 9 usuários de teste
- ✅ Popular catálogo com 100+ serviços

### 2️⃣ **Iniciar o Sistema:**

```
INICIAR_API_8001.bat
```

### 3️⃣ **Acessar:**

- **Frontend**: http://localhost:8001/app
- **API Docs**: http://localhost:8001/docs
- **Health**: http://localhost:8001/health

---

## 👤 USUÁRIOS DE TESTE

| Tipo | Email | Senha | Descrição |
|------|-------|-------|-----------|
| **Admin** | admin@zeladoria.com | admin123 | Administrador do sistema |
| **SEURB** | seurb@zeladoria.com | seurb123 | Secretaria de Urbanismo |
| **SESAN** | sesan@zeladoria.com | sesan123 | Secretaria de Saneamento |
| **SEMOB** | semob@zeladoria.com | semob123 | Secretaria de Mobilidade |
| **SEMMA** | semma@zeladoria.com | semma123 | Secretaria de Meio Ambiente |
| **SESMA** | sesma@zeladoria.com | sesma123 | Secretaria de Saúde |
| **Gestor** | gestor@zeladoria.com | gestor123 | Gestor municipal |
| **Equipe** | equipe@zeladoria.com | equipe123 | Equipe de campo |
| **Cidadão** | cidadao@zeladoria.com | cidadao123 | Cidadão comum |

---

## 📦 ESTRUTURA DO SISTEMA

### **Secretarias Municipais:**
- 🏗️ **SEURB** - Urbanismo (obras, pavimentação, iluminação)
- ♻️ **SESAN** - Saneamento (limpeza, coleta de lixo)
- 🚗 **SEMOB** - Mobilidade (trânsito, transporte)
- 🌳 **SEMMA** - Meio Ambiente (áreas verdes, fiscalização)
- 🏥 **SESMA** - Saúde (unidades de saúde, vigilância)

### **Catálogo de Serviços:**
- 100+ serviços cadastrados
- SLA (Service Level Agreement) definido
- Prioridades (Emergencial, Alta, Média, Baixa)
- Custos (Gratuito ou Pago)
- Categorias organizadas

---

## 🛠️ SCRIPTS DISPONÍVEIS

### **Setup Inicial:**
```
SETUP_COMPLETO.bat           - Setup completo do zero
CRIAR_SECRETARIAS.bat        - Criar apenas secretarias
CRIAR_USUARIOS.bat           - Criar apenas usuários
CRIAR_TABELA.bat            - Criar tabela de serviços
popular_simples.bat          - Popular catálogo de serviços
```

### **Uso Diário:**
```
INICIAR_API_8001.bat        - Iniciar API na porta 8001
INICIAR_API_8000.bat        - Iniciar API na porta 8000
MENU_SIMPLES.bat            - Menu interativo
```

### **Instalação:**
```
INSTALAR_TUDO_FALTANDO.bat  - Instalar todas dependências
INSTALAR_REQUIREMENTS.bat    - Instalar via requirements.txt
```

---

## 📚 ENDPOINTS DA API

### **Autenticação:**
- POST `/api/auth/login` - Login
- POST `/api/auth/register` - Registro
- GET `/api/auth/me` - Usuário logado

### **Secretarias:**
- GET `/api/secretarias/` - Listar todas
- GET `/api/secretarias/{id}` - Obter por ID
- GET `/api/secretarias/sigla/{sigla}` - Obter por sigla
- POST `/api/secretarias/` - Criar
- PUT `/api/secretarias/{id}` - Atualizar
- DELETE `/api/secretarias/{id}` - Deletar

### **Catálogo de Serviços:**
- GET `/api/servicos/` - Listar serviços
- GET `/api/servicos/{id}` - Detalhes
- GET `/api/servicos/dashboard` - Dashboard
- GET `/api/servicos/categorias/listar` - Categorias
- POST `/api/servicos/` - Criar serviço
- PUT `/api/servicos/{id}` - Atualizar
- DELETE `/api/servicos/{id}` - Deletar

### **Chamados:**
- GET `/api/chamados/` - Listar
- POST `/api/chamados/` - Criar
- GET `/api/chamados/{id}` - Detalhes
- PUT `/api/chamados/{id}` - Atualizar
- DELETE `/api/chamados/{id}` - Deletar

---

## 💻 DESENVOLVIMENTO

### **Iniciar em modo dev:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### **Acessar diferentes interfaces:**
- **Frontend**: http://localhost:8001/app
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health

---

## 🎨 FRONTEND

O frontend está localizado em `/frontend/index.html`

### **Características:**
- ✅ Layout inspirado na Prefeitura de Belém
- ✅ Responsivo (mobile, tablet, desktop)
- ✅ Login funcional
- ✅ Cards das secretarias
- ✅ Cores institucionais (azul e verde)
- ✅ Usuários de teste visíveis

---

## 🗄️ BANCO DE DADOS

### **Tabelas:**
- `usuarios` - Usuários do sistema
- `secretarias` - Secretarias municipais
- `servicos_secretaria` - Catálogo de serviços
- `chamados` - Chamados/solicitações
- `categorias` - Categorias de chamados
- `bairros` - Bairros de Belém

### **Banco atual:** SQLite (`zeladoria.db`)

---

## 🔧 RESOLUÇÃO DE PROBLEMAS

### **Erro: "No module named 'X'"**
Execute:
```
INSTALAR_TUDO_FALTANDO.bat
```

### **Erro: "Secretarias não aparecem"**
Execute:
```
CRIAR_SECRETARIAS.bat
```

### **Erro: "Não consigo fazer login"**
Execute:
```
CRIAR_USUARIOS.bat
```

### **Porta 8001 ocupada:**
Use:
```
INICIAR_API_8000.bat
```

---

## 📞 SUPORTE

- **Documentação da API**: http://localhost:8001/docs
- **Status do Sistema**: http://localhost:8001/health
- **Logs**: Console onde a API está rodando

---

## ✅ CHECKLIST FINAL

- [ ] Dependências instaladas (`INSTALAR_TUDO_FALTANDO.bat`)
- [ ] Setup completo executado (`SETUP_COMPLETO.bat`)
- [ ] API rodando (`INICIAR_API_8001.bat`)
- [ ] Frontend acessível (http://localhost:8001/app)
- [ ] Login funcionando (admin@zeladoria.com / admin123)
- [ ] Secretarias aparecendo na tela
- [ ] API docs acessível (http://localhost:8001/docs)

---

## 🎉 PRONTO!

**Seu sistema está completo e funcionando!**

Acesse: **http://localhost:8001/app**

Login de teste: **admin@zeladoria.com** / **admin123**

---

*Sistema desenvolvido para a Prefeitura Municipal de Belém/PA*
*Versão 2.0 - 2025*
