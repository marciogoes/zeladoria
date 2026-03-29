# 🚀 API de Tarefas - FastAPI + SQLite

API RESTful simples e funcional para gerenciamento de tarefas, construída com FastAPI e SQLite.

## 📋 Funcionalidades

- ✅ **CRUD Completo** de Tarefas
- ✅ **SQLite** como banco de dados
- ✅ **Validação** automática com Pydantic
- ✅ **Documentação** interativa automática (Swagger)
- ✅ **Arquitetura limpa** e organizada

## 🗂️ Estrutura do Projeto

```
backend-fastapi/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py       # Configuração do SQLite
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py           # Modelo SQLAlchemy
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py          # Endpoints da API
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py           # Validação Pydantic
│   └── __init__.py
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências
├── .gitignore
└── README.md
```

## 🔧 Instalação

### 1️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

### 2️⃣ Ativar ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

## ▶️ Como Executar

```bash
uvicorn main:app --reload
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação Interativa

Após iniciar o servidor, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔌 Endpoints Disponíveis

### Tarefas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/tasks/` | Criar nova tarefa |
| `GET` | `/tasks/` | Listar todas as tarefas |
| `GET` | `/tasks/{id}` | Buscar tarefa por ID |
| `PUT` | `/tasks/{id}` | Atualizar tarefa |
| `DELETE` | `/tasks/{id}` | Deletar tarefa |
| `PATCH` | `/tasks/{id}/complete` | Marcar como concluída |

## 💡 Exemplos de Uso

### Criar Tarefa

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI",
    "description": "Aprender a criar APIs com FastAPI",
    "completed": false
  }'
```

### Listar Tarefas

```bash
curl -X GET "http://localhost:8000/tasks/"
```

### Buscar Tarefa

```bash
curl -X GET "http://localhost:8000/tasks/1"
```

### Atualizar Tarefa

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI - Atualizado",
    "completed": true
  }'
```

### Deletar Tarefa

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## 📦 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **SQLite** - Banco de dados leve
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

## 🚀 Próximos Passos

- [ ] Adicionar autenticação JWT
- [ ] Implementar filtros e busca
- [ ] Adicionar paginação
- [ ] Criar testes unitários
- [ ] Dockerizar aplicação
- [ ] Deploy em produção

## 📝 Licença

Este projeto está sob a licença MIT.

## 👤 Autor

Desenvolvido como exemplo de estrutura FastAPI + SQLite.

---

**Dúvidas?** Consulte a documentação interativa em `/docs` 🎯
