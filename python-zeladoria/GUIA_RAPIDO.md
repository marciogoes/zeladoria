# 🚀 GUIA RÁPIDO - Sistema de Zeladoria Urbana

## ⚡ INSTALAÇÃO EM 5 MINUTOS

### 1️⃣ Abrir PowerShell

Pressione `Win + X` e escolha "Windows PowerShell"

### 2️⃣ Copiar e Colar

```powershell
cd C:\Users\marci\OneDrive\Documentos\Projetos\zeladoria\python-zeladoria
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python main.py
```

### 3️⃣ Abrir Navegador

```
http://localhost:8000/app
```

### 4️⃣ Fazer Login

Clique em um dos botões coloridos:
- 👤 **Cidadão** - Ver e criar chamados
- 👷 **Equipe** - Atualizar status
- 📊 **Gestor** - Ver dashboard

---

## 🎯 O QUE VOCÊ TEM

✅ **Backend Python + FastAPI**
- API RESTful completa
- Autenticação JWT
- Upload de fotos
- SQLite database

✅ **Frontend Moderno**
- Interface intuitiva
- Design profissional
- 100% funcional
- Responsivo

✅ **Dados de Teste**
- 4 usuários
- 8 categorias
- 10 bairros
- 3 chamados

---

## 📱 FUNCIONALIDADES

### Para Cidadãos
- ➕ Criar chamados com foto
- 📋 Ver meus chamados
- 🔍 Buscar e filtrar
- ⭐ Avaliar atendimento

### Para Equipe
- 📞 Ver todos os chamados
- ✏️ Atualizar status
- 📸 Adicionar foto depois
- 👥 Atribuir responsável

### Para Gestores
- 📊 Dashboard completo
- 📈 Estatísticas em tempo real
- 🏆 Top categorias e bairros
- 👥 Gerenciar usuários

---

## 🔑 LOGINS

```
Cidadão:  pedro.almeida@email.com / senha123
Equipe:   joao.silva@belem.pa.gov.br / senha123
Gestor:   maria.santos@belem.pa.gov.br / senha123
Admin:    admin@belem.pa.gov.br / senha123
```

---

## 📚 DOCUMENTAÇÃO

- `README.md` - Visão geral
- `SISTEMA_COMPLETO.md` - Documentação backend
- `FRONTEND_PRONTO.md` - Documentação frontend
- `http://localhost:8000/docs` - API Swagger

---

## 🆘 PROBLEMAS?

### Erro: "python não é reconhecido"
```powershell
# Verifique se Python está instalado
python --version
```

### Erro: "pip não funciona"
```powershell
# Certifique-se de estar no venv
venv\Scripts\activate
```

### Porta 8000 ocupada
```powershell
# Usar outra porta
uvicorn main:app --reload --port 8001
```

### Frontend não carrega
```powershell
# Verificar se backend está rodando
# Abrir: http://localhost:8000/health
```

---

## 📞 CONTATO

Sistema desenvolvido para:
**Prefeitura Municipal de Belém/PA**

---

## ✨ PRONTO PARA USAR!

Seu sistema está **100% funcional**!

**Comandos:**
```powershell
# Iniciar
python main.py

# Acessar
http://localhost:8000/app

# Parar
CTRL + C
```

---

**Divirta-se! 🎉**
