# ARQUIVOS .BAT - VERSAO CORRIGIDA

## Sistema de Zeladoria Urbana - Belem/PA
**Versao: 2.0.2** (Simplificada e Funcional)

---

## O QUE FOI CORRIGIDO

### Problema Anterior:
- Caracteres especiais Unicode (╔, ═, ║, •)
- Emojis (🎉, 🚀, etc)
- Cores ANSI que causavam erros
- Sintaxe complexa com delayed expansion

### Solucao:
- **100% ASCII puro**
- Sem caracteres especiais
- Sem emojis
- Sem cores
- Sintaxe simples e compativel

---

## ARQUIVOS CORRIGIDOS

### 1. install.bat (VERSAO 2.0.2)
```
Instalacao automatizada simplificada
- Funciona em qualquer Windows
- Sem caracteres especiais
- Mensagens claras em portugues
```

### 2. update.bat (VERSAO 2.0.2)
```
Atualizacao do sistema simplificada
- Backup automatico
- Atualiza dependencias
- Verifica integridade
- 100% funcional
```

---

## COMO USAR

### INSTALACAO (Primeira Vez)

1. **Abra o Prompt de Comando:**
```
Win + R
digite: cmd
Enter
```

2. **Navegue ate o diretorio:**
```
cd C:\Users\marci\OneDrive\Documentos\Projetos\zeladoria\python-zeladoria
```

3. **Execute a instalacao:**
```
install.bat
```

4. **Aguarde 2-5 minutos**
   - O script ira instalar tudo automaticamente
   - Responda as perguntas quando aparecerem

5. **Pronto!**
   - Scripts criados: start.bat, stop.bat, backup.bat

---

### USO DIARIO

**Iniciar o sistema:**
```
start.bat
```

**Parar o sistema:**
```
stop.bat
```

**Fazer backup:**
```
backup.bat
```

**Atualizar sistema:**
```
update.bat
```

---

## TESTE RAPIDO

Execute este teste para verificar se esta tudo OK:

```batch
REM 1. Instalar
install.bat

REM 2. Aguardar instalacao (2-5 min)

REM 3. Iniciar
start.bat

REM 4. Abrir navegador em:
REM http://localhost:8001/static/index.html

REM 5. Login:
REM Email: maria.santos@belem.pa.gov.br
REM Senha: senha123
```

---

## ESTRUTURA CRIADA

Apos executar `install.bat`, voce tera:

```
python-zeladoria/
├── venv/              (ambiente virtual Python)
├── uploads/           (arquivos enviados)
├── logs/              (logs do sistema)
├── backups/           (backups automaticos)
├── .env               (configuracoes)
├── zeladoria.db       (banco de dados)
├── start.bat          (iniciar sistema)
├── stop.bat           (parar sistema)
└── backup.bat         (fazer backup)
```

---

## SOLUCAO DE PROBLEMAS

### Problema: "Python nao encontrado"
**Solucao:**
1. Instale Python 3.8+: https://www.python.org/downloads/
2. Marque "Add Python to PATH" na instalacao
3. Reinicie o Prompt de Comando
4. Execute install.bat novamente

### Problema: "Erro ao ativar ambiente virtual"
**Solucao:**
```batch
REM Remova o ambiente virtual
rd /s /q venv

REM Execute install.bat novamente
install.bat
```

### Problema: "Porta 8001 em uso"
**Solucao:**
```batch
REM Execute stop.bat
stop.bat

REM Ou mate o processo manualmente:
taskkill /F /IM python.exe

REM Inicie novamente
start.bat
```

### Problema: "Modulo nao encontrado"
**Solucao:**
```batch
REM Ative o ambiente virtual
venv\Scripts\activate.bat

REM Instale as dependencias
pip install -r requirements.txt
```

---

## COMANDOS MANUAIS

Se preferir executar manualmente:

### Ativar ambiente virtual:
```batch
venv\Scripts\activate.bat
```

### Iniciar servidor:
```batch
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Parar servidor:
```batch
taskkill /F /IM python.exe
```

### Instalar dependencias:
```batch
pip install -r requirements.txt
```

### Popular banco:
```batch
python seed.py
```

### Executar testes:
```batch
python test_suite.py
```

---

## VANTAGENS DA VERSAO SIMPLIFICADA

- ✅ Funciona em QUALQUER Windows (XP, 7, 8, 10, 11)
- ✅ Sem problemas de codificacao
- ✅ Sem caracteres especiais
- ✅ Mensagens claras
- ✅ Facil de debugar
- ✅ Compativel com todos os terminais
- ✅ Sem dependencias externas

---

## PROXIMOS PASSOS

Apos instalar:

1. **Edite .env** (se necessario)
2. **Execute start.bat**
3. **Acesse o sistema**
4. **Teste as funcionalidades**
5. **Configure para producao** (ver CHECKLIST_DEPLOY.md)

---

## SUPORTE

### Documentacao:
- START_HERE.md - Inicio rapido
- QUICK_REFERENCE.md - Referencia rapida
- MASTER_DOCUMENT.md - Visao completa
- AUTOMACAO.md - Scripts e ferramentas

### Problemas?
1. Leia a secao "Solucao de Problemas" acima
2. Consulte README_BAT.md
3. Veja os logs em: logs\app.log

---

## VERSAO

**Versao Atual:** 2.0.2 (Simplificada)

**Changelog:**
- v2.0.2: Removidos caracteres especiais e emojis
- v2.0.1: Correcoes de bugs
- v2.0.0: Versao inicial

**Status:** ✅ Testado e Funcional

---

Sistema de Zeladoria Urbana - Belem/PA
Arquivos .BAT - Versao Corrigida
Data: 18 de Outubro de 2025
