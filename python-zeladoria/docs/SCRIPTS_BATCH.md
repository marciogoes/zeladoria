# 🖥️ Scripts Batch (.bat) - Catálogo de Serviços

## 🎯 Para Começar - Execute 1 Comando

```cmd
catalogo.bat
```

Este é o **menu principal** que te guia por todas as opções!

---

## 📋 Scripts Disponíveis (9 arquivos .bat)

### 🎮 Menu Principal

#### `catalogo.bat` ⭐ **COMECE POR AQUI**
Menu interativo com todas as opções:
- Setup completo
- Criar tabela
- Popular banco
- Ver estatísticas
- Listar serviços
- Buscar
- Iniciar API

**Como usar:**
```cmd
catalogo.bat
```

---

### 🚀 Setup e Instalação

#### `setup_catalogo.bat` - Setup Completo Automático
Executa TUDO em sequência:
1. Cria a tabela
2. Verifica criação
3. Popula com 100+ serviços
4. Mostra estatísticas

**Como usar:**
```cmd
setup_catalogo.bat
```

**⚠️ ANTES de executar:** Ajuste os IDs das secretarias em `app\seeds\seed_servicos.py`

---

#### `criar_tabela.bat` - Criar Tabela
Cria apenas a tabela `servicos_secretaria` no banco.

**Como usar:**
```cmd
criar_tabela.bat
```

---

#### `popular_catalogo.bat` - Popular Banco
Insere 100+ serviços no banco de dados.

**Como usar:**
```cmd
popular_catalogo.bat
```

**Pré-requisito:** Tabela criada + IDs ajustados

---

### 📊 Consultas e Visualização

#### `listar_servicos.bat` - Listar Todos os Serviços
Mostra lista completa dos serviços cadastrados.

**Como usar:**
```cmd
listar_servicos.bat
```

---

#### `ver_estatisticas.bat` - Estatísticas
Mostra estatísticas completas:
- Total de serviços
- Por prioridade
- Por status
- Por categoria
- Custos

**Como usar:**
```cmd
ver_estatisticas.bat
```

---

#### `buscar_servico.bat` - Buscar
Busca serviços por termo (código, nome, descrição).

**Como usar:**
```cmd
buscar_servico.bat
```

Vai pedir o termo de busca interativamente.

---

### 🌐 API

#### `iniciar_api.bat` - Iniciar Servidor
Inicia o servidor FastAPI na porta 8000.

**Como usar:**
```cmd
iniciar_api.bat
```

**Acesse:**
- API: http://localhost:8000/api/servicos/
- Docs: http://localhost:8000/docs

**Para parar:** Pressione `CTRL+C`

---

#### `testar_api.bat` - Testar Endpoints
Testa todos os principais endpoints da API.

**Como usar:**
```cmd
# Janela 1: Iniciar API
iniciar_api.bat

# Janela 2: Testar
testar_api.bat
```

Testa:
- Listar serviços
- Dashboard
- Categorias
- Busca
- Autocomplete

---

### 📖 Ajuda

#### `LEIA-ME.bat` - Instruções
Mostra todas as instruções e comandos disponíveis.

**Como usar:**
```cmd
LEIA-ME.bat
```

---

## 🎯 Fluxo de Trabalho Recomendado

### Primeira Vez (Setup Inicial)

```cmd
# 1. Ver instruções
LEIA-ME.bat

# 2. Editar IDs das secretarias
notepad app\seeds\seed_servicos.py

# 3. Setup completo
setup_catalogo.bat

# 4. Iniciar API
iniciar_api.bat

# 5. Testar (em outra janela)
testar_api.bat
```

### Uso Diário

```cmd
# Opção 1: Menu interativo
catalogo.bat

# Opção 2: Comandos diretos
listar_servicos.bat
buscar_servico.bat
ver_estatisticas.bat
```

---

## ⚙️ Configuração Necessária

### Antes de Popular o Banco

Edite `app\seeds\seed_servicos.py`:

```python
secretarias_map = {
    "SEURB": 1,   # ← ID real da sua tabela secretarias
    "SESAN": 2,   # ← ID real da sua tabela secretarias
    "SEMOB": 3,   # ← ID real da sua tabela secretarias
    "SEMMA": 4,   # ← ID real da sua tabela secretarias
    "SESMA": 5,   # ← ID real da sua tabela secretarias
}
```

**Como descobrir os IDs:**

```sql
SELECT id, nome FROM secretarias ORDER BY id;
```

---

## 🔧 Troubleshooting

### "Python não é reconhecido como comando"

**Solução:** Adicione Python ao PATH do Windows ou use caminho completo:
```cmd
C:\Python311\python.exe manage_catalogo.py
```

### "Módulo não encontrado"

**Solução:** Execute os bats a partir da raiz do projeto:
```cmd
cd C:\caminho\para\python-zeladoria
catalogo.bat
```

### "Erro ao conectar ao banco"

**Solução:** Verifique `app\database\database.py`:
- URL do banco está correta?
- Banco está rodando?
- Credenciais corretas?

### "IDs de secretaria não existem"

**Solução:** 
1. Veja os IDs reais: `SELECT * FROM secretarias`
2. Ajuste em `app\seeds\seed_servicos.py`
3. Execute `popular_catalogo.bat` novamente

---

## 📂 Organização dos Arquivos

```
python-zeladoria/
│
├── 📁 Scripts Batch (.bat)
│   ├── catalogo.bat              ⭐ Menu principal
│   ├── setup_catalogo.bat        🚀 Setup completo
│   ├── criar_tabela.bat          🔧 Criar tabela
│   ├── popular_catalogo.bat      🌱 Popular dados
│   ├── listar_servicos.bat       📋 Listar
│   ├── ver_estatisticas.bat      📊 Stats
│   ├── buscar_servico.bat        🔍 Buscar
│   ├── iniciar_api.bat           🌐 API
│   ├── testar_api.bat            🧪 Testes
│   └── LEIA-ME.bat               📖 Help
│
├── 📁 Python Scripts
│   ├── manage_catalogo.py        CLI Python
│   ├── migrations/               Migrações
│   ├── app/                      Código fonte
│   └── docs/                     Documentação
│
└── README_CATALOGO.md            📚 Docs
```

---

## 🎨 Customização

### Adicionar Nova Opção no Menu

Edite `catalogo.bat`:

```batch
if "%opcao%"=="10" (
    echo Executando minha tarefa...
    python meu_script.py
    goto menu
)
```

### Criar Seu Próprio Batch

```batch
@echo off
chcp 65001 >nul
echo Meu Script
python manage_catalogo.py stats
pause
```

---

## ✅ Checklist de Validação

Execute em sequência para validar tudo:

- [ ] `LEIA-ME.bat` - Ver instruções
- [ ] Editar IDs em `seed_servicos.py`
- [ ] `criar_tabela.bat` - Criar tabela
- [ ] `popular_catalogo.bat` - Popular
- [ ] `ver_estatisticas.bat` - Ver stats
- [ ] `listar_servicos.bat` - Listar
- [ ] `buscar_servico.bat` - Buscar
- [ ] `iniciar_api.bat` - API
- [ ] `testar_api.bat` - Testar

**Se todos funcionarem: ✅ Sistema OK!**

---

## 🎉 Pronto para Usar!

Basta executar:

```cmd
catalogo.bat
```

E seguir o menu interativo! 🚀

---

**Sistema**: Zeladoria Urbana - Belém/PA  
**Versão**: 1.0  
**Data**: Outubro 2025
