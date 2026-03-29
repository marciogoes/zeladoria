# 🏛️ SISTEMA DE SECRETARIAS MUNICIPAIS

## 📦 SISTEMA DE ZELADORIA URBANA - BELÉM/PA

**Versão:** 2.1.0  
**Data:** 18 de Outubro de 2025  
**Novidade:** Sistema de Gestão por Secretarias

---

## 🎯 O QUE MUDOU

### **ANTES:**
- ❌ Apenas um gestor geral
- ❌ Todas as categorias sem responsável específico
- ❌ Equipe genérica

### **AGORA:**
- ✅ **15 Secretarias Municipais** reais de Belém
- ✅ **Cada categoria** associada a uma secretaria responsável
- ✅ **Perfil SECRETARIA** com dashboard próprio
- ✅ **Gestão descentralizada** por órgão
- ✅ **Perfil GESTOR** exclusivo para Prefeito/Coordenador Geral

---

## 🏛️ SECRETARIAS INCLUÍDAS

### **Administração e Gestão:**
- **SEMAD** - Secretaria Municipal de Administração
- **SEGEP** - Coordenadoria Geral de Planejamento e Gestão

### **Finanças e Economia:**
- **SEFIN** - Secretaria Municipal de Finanças
- **SECON** - Secretaria Municipal de Economia

### **Infraestrutura e Urbanismo:**
- **SEURB** - Secretaria Municipal de Urbanismo
- **SESAN** - Secretaria Municipal de Saneamento
- **SEHAB** - Secretaria Municipal de Habitação

### **Saúde e Bem-Estar:**
- **SESMA** - Secretaria Municipal de Saúde
- **SEMULHER** - Secretaria Municipal da Mulher

### **Educação:**
- **SEMEC** - Secretaria Municipal de Educação

### **Meio Ambiente:**
- **SEMMA** - Secretaria Municipal de Meio Ambiente

### **Outras Secretarias:**
- **SEMAJ** - Secretaria Municipal de Assuntos Jurídicos
- **SEJEL** - Secretaria Municipal de Esporte, Juventude e Lazer

### **Órgãos e Autarquias:**
- **GMB** - Guarda Municipal de Belém
- **OGM** - Ouvidoria Geral do Município

---

## 📋 ASSOCIAÇÃO: CATEGORIAS → SECRETARIAS

### **SEURB (Urbanismo):**
- Buraco na via
- Iluminação pública
- Calçada danificada
- Sinalização

### **SESAN (Saneamento):**
- Lixo acumulado
- Esgoto
- Coleta de lixo

### **SEMMA (Meio Ambiente):**
- Poda de árvore
- Área verde
- Animal abandonado

### **SESMA (Saúde):**
- Foco de dengue

### **SEJEL (Esporte e Lazer):**
- Equipamento público

### **GMB (Guarda Municipal):**
- Segurança pública

### **SEMEC (Educação):**
- Infraestrutura escolar

### **SEHAB (Habitação):**
- Habitação irregular

---

## 👥 PERFIS DE USUÁRIO

### **1. CIDADAO** (Munícipe)
```
✅ Criar chamados
✅ Acompanhar seus chamados
✅ Avaliar atendimentos
✅ Ver histórico pessoal
```

### **2. EQUIPE** (Operador de Campo)
```
✅ Ver chamados atribuídos
✅ Atualizar status
✅ Adicionar observações
✅ Resolver chamados
```

### **3. SECRETARIA** (Gestão por Órgão) ⭐ NOVO
```
✅ Ver APENAS chamados da sua secretaria
✅ Dashboard específico da secretaria
✅ Gerenciar chamados do seu órgão
✅ Atribuir para equipes
✅ Relatórios da secretaria
✅ Métricas por categoria
```

### **4. GESTOR** (Prefeito/Coordenador Geral)
```
✅ Ver TODOS os chamados
✅ Dashboard geral consolidado
✅ Comparação entre secretarias
✅ Relatórios gerenciais
✅ Métricas globais
✅ Visão estratégica
```

### **5. ADMIN** (Administrador do Sistema)
```
✅ Gerenciar usuários
✅ Configurar sistema
✅ Criar secretarias
✅ Gerenciar categorias
✅ Acesso total
```

---

## 🚀 COMO USAR

### **OPÇÃO 1: INSTALAÇÃO NOVA (Recomendado)**

```batch
REM 1. Remova o banco atual (se existir)
del zeladoria.db

REM 2. Execute o seed atualizado
venv\Scripts\activate.bat
python seed.py

REM 3. Reinicie o backend
stop.bat
start.bat
```

**Resultado:** Sistema novo com 15 secretarias + usuários de teste

---

### **OPÇÃO 2: MIGRAR BANCO EXISTENTE**

```batch
REM 1. Execute o script de migração
venv\Scripts\activate.bat
python migrar_secretarias.py

REM 2. Siga as instruções na tela
REM (Será criado backup automático)

REM 3. Reinicie o backend
stop.bat
start.bat
```

**Resultado:** Banco atual + 15 secretarias + associações

---

## 👤 USUÁRIOS DE TESTE

### **Secretarias (Perfil: SECRETARIA):**
```
SEURB (Urbanismo):
Email: carlos.mendes@seurb.belem.pa.gov.br
Senha: senha123

SESAN (Saneamento):
Email: ana.costa@sesan.belem.pa.gov.br
Senha: senha123

SEMMA (Meio Ambiente):
Email: roberto.lima@semma.belem.pa.gov.br
Senha: senha123
```

### **Gestor Geral (Perfil: GESTOR):**
```
Email: maria.santos@belem.pa.gov.br
Senha: senha123
```

---

## 📊 DIFERENÇAS: SECRETARIA vs GESTOR

### **Dashboard SECRETARIA:**
```
✅ Vê apenas chamados da SUA secretaria
✅ Métricas específicas do órgão
✅ Top categorias da secretaria
✅ Performance da equipe da secretaria
✅ SLA por categoria do órgão
```

**Exemplo:** Usuário da SEURB vê apenas:
- Buraco na via
- Iluminação pública
- Calçada danificada
- Sinalização

---

### **Dashboard GESTOR:**
```
✅ Vê chamados de TODAS as secretarias
✅ Métricas consolidadas
✅ Comparação entre secretarias
✅ Ranking de performance
✅ Visão estratégica global
```

**Exemplo:** Gestor vê:
- TODAS as categorias
- Comparação SEURB vs SESAN vs SEMMA
- Performance geral do município

---

## 🎨 FUNCIONALIDADES POR PERFIL

### **CIDADAO:**
- ✅ Abrir chamado
- ✅ Escolher categoria (automático → secretaria)
- ✅ Acompanhar protocolo
- ✅ Avaliar atendimento

### **EQUIPE:**
- ✅ Listar chamados atribuídos
- ✅ Atualizar status
- ✅ Adicionar fotos/observações
- ✅ Marcar como resolvido

### **SECRETARIA:**
- ✅ Dashboard da secretaria
- ✅ Ver chamados do órgão
- ✅ Atribuir para equipes
- ✅ Priorizar chamados
- ✅ Relatórios setoriais
- ✅ Exportar dados da secretaria

### **GESTOR:**
- ✅ Dashboard consolidado
- ✅ Ver todos os chamados
- ✅ Comparar secretarias
- ✅ Relatórios gerenciais
- ✅ Exportar dados gerais
- ✅ Análise estratégica

### **ADMIN:**
- ✅ Tudo do Gestor +
- ✅ Criar/editar secretarias
- ✅ Gerenciar usuários
- ✅ Configurar categorias
- ✅ Associar categorias ↔ secretarias

---

## 🔄 FLUXO DE TRABALHO

### **1. Cidadão Abre Chamado:**
```
Cidadão → Escolhe categoria "Buraco na via"
Sistema → Associa automaticamente à SEURB
```

### **2. Secretaria Recebe:**
```
SEURB → Vê novo chamado no dashboard
SEURB → Atribui para equipe de campo
SEURB → Define prioridade
```

### **3. Equipe Atende:**
```
Equipe → Recebe notificação
Equipe → Vai ao local
Equipe → Resolve problema
Equipe → Marca como "Resolvido"
```

### **4. Cidadão Avalia:**
```
Cidadão → Recebe notificação
Cidadão → Avalia atendimento (1-5 ⭐)
Cidadão → Deixa comentário
```

### **5. Gestor Monitora:**
```
Gestor → Vê performance de todas secretarias
Gestor → Identifica gargalos
Gestor → Toma decisões estratégicas
```

---

## 📈 BENEFÍCIOS

### **Para as Secretarias:**
- ✅ Autonomia na gestão
- ✅ Foco nos chamados do órgão
- ✅ Métricas específicas
- ✅ Responsabilidade clara

### **Para o Gestor:**
- ✅ Visão consolidada
- ✅ Comparação entre órgãos
- ✅ Tomada de decisão estratégica
- ✅ Identificação de problemas

### **Para os Cidadãos:**
- ✅ Atendimento mais rápido
- ✅ Responsável identificado
- ✅ Transparência
- ✅ Acompanhamento claro

---

## 🛠️ CONFIGURAÇÃO

### **Criar Nova Secretaria:**

```python
from app.models import Secretaria
from app.database import SessionLocal

db = SessionLocal()

nova_secretaria = Secretaria(
    sigla="NOVA",
    nome="Secretaria Nova",
    email="nova@belem.pa.gov.br",
    telefone="(91) 3242-XXXX"
)

db.add(nova_secretaria)
db.commit()
```

### **Associar Categoria à Secretaria:**

```python
from app.models import Categoria, Secretaria

secretaria = db.query(Secretaria).filter_by(sigla="SEURB").first()
categoria = db.query(Categoria).filter_by(nome="Buraco na via").first()

categoria.secretaria_id = secretaria.id
db.commit()
```

### **Criar Usuário de Secretaria:**

```python
from app.models import Usuario, TipoUsuario

usuario = Usuario(
    nome="João Silva - SEURB",
    email="joao.silva@seurb.belem.pa.gov.br",
    senha_hash=criar_hash_senha("senha123"),
    tipo=TipoUsuario.SECRETARIA,
    secretaria_id=secretaria.id
)

db.add(usuario)
db.commit()
```

---

## 📋 CHECKLIST DE IMPLANTAÇÃO

### **Fase 1: Preparação**
- [ ] Fazer backup do banco atual
- [ ] Revisar lista de secretarias
- [ ] Definir categorias por secretaria
- [ ] Preparar lista de usuários

### **Fase 2: Migração**
- [ ] Executar `python migrar_secretarias.py`
- [ ] Verificar secretarias criadas
- [ ] Verificar associações
- [ ] Testar logins

### **Fase 3: Configuração**
- [ ] Criar usuários das secretarias
- [ ] Configurar permissões
- [ ] Testar dashboards
- [ ] Ajustar SLAs por categoria

### **Fase 4: Treinamento**
- [ ] Treinar equipes das secretarias
- [ ] Treinar gestores
- [ ] Documentar processos
- [ ] Criar manuais

### **Fase 5: Go-Live**
- [ ] Comunicar mudanças
- [ ] Ativar sistema
- [ ] Monitorar uso
- [ ] Coletar feedback

---

## 🎯 PRÓXIMOS PASSOS

1. **Execute a migração:**
   ```batch
   python migrar_secretarias.py
   ```

2. **Reinicie o backend:**
   ```batch
   stop.bat
   start.bat
   ```

3. **Teste os logins:**
   - Secretaria: carlos.mendes@seurb.belem.pa.gov.br
   - Gestor: maria.santos@belem.pa.gov.br

4. **Explore os dashboards:**
   - Dashboard da SEURB (apenas categorias de urbanismo)
   - Dashboard do Gestor (todas as categorias)

5. **Customize:**
   - Adicione mais secretarias se necessário
   - Ajuste categorias
   - Crie mais usuários

---

## 📞 SUPORTE

**Dúvidas sobre:**
- Migração → Ver `migrar_secretarias.py`
- Novos usuários → Ver `seed.py`
- Configuração → Ver documentação dos modelos

---

**Sistema de Zeladoria Urbana - Belém/PA**  
**Sistema de Secretarias Municipais**  
**Versão:** 2.1.0  
**Data:** 18 de Outubro de 2025

```
🏛️ 15 SECRETARIAS MUNICIPAIS
👥 5 PERFIS DE USUÁRIO
🔗 CATEGORIAS ASSOCIADAS
📊 DASHBOARDS ESPECÍFICOS

GESTÃO DESCENTRALIZADA E EFICIENTE!
```
