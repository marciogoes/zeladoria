# 🎯 FUNCIONALIDADES POR PERFIL - Sistema de Zeladoria

## 👤 PERFIL: CIDADÃO

### O que o cidadão pode fazer:

✅ **Criar Chamados**
- Reportar problemas urbanos com título, descrição e foto
- Adicionar localização (endereço, latitude, longitude)
- Escolher categoria (Iluminação, Buracos, Lixo, etc.)
- Receber protocolo automaticamente

✅ **Ver Seus Chamados**
- Lista apenas os chamados que ELE criou
- Filtrar por status (aberto, em andamento, resolvido, cancelado)
- Filtrar por prioridade (baixa, média, alta, crítica)
- Buscar por protocolo ou título

✅ **Acompanhar Status**
- Ver detalhes completos do chamado
- Acompanhar progresso em tempo real
- Ver fotos antes e depois (quando equipe adicionar)
- Ver responsável atribuído

✅ **Avaliar Serviço**
- Quando chamado for resolvido, pode avaliar de 1 a 5 estrelas
- Deixar comentário sobre o atendimento
- Ajudar a melhorar o serviço público

### Interface do Cidadão:
- 📞 **Chamados** - Ver seus chamados
- ➕ **Novo Chamado** - Reportar problema
- ❌ **Dashboard** - NÃO tem acesso

---

## 👷 PERFIL: EQUIPE (Campo)

### O que a equipe pode fazer:

✅ **Ver Todos os Chamados**
- Acesso a TODOS os chamados da cidade
- Não está limitado aos próprios chamados
- Ver quem criou cada chamado

✅ **Gerenciar Chamados**
- **Atualizar Status:**
  - Aberto → Em Andamento
  - Em Andamento → Resolvido
  - Qualquer → Cancelado
- Ver histórico de mudanças
- Adicionar fotos do serviço concluído

✅ **Filtros Avançados**
- Por status para ver o que precisa atenção
- Por prioridade para atender casos críticos primeiro
- Por bairro para otimizar rotas
- Buscar por protocolo específico

✅ **Visualizar Detalhes**
- Todas as informações do chamado
- Foto do problema reportada pelo cidadão
- Localização no mapa (latitude/longitude)
- Histórico de atualizações

### Interface da Equipe:
- 📞 **Chamados** - Ver TODOS os chamados
- ➕ **Novo Chamado** - Criar chamado
- ❌ **Dashboard** - NÃO tem acesso

---

## 📊 PERFIL: GESTOR

### O que o gestor pode fazer:

✅ **Dashboard Completo**
- **Cards de Estatísticas:**
  - Total de Chamados
  - Chamados Em Andamento
  - Chamados Resolvidos
  - Avaliação Média do Serviço

✅ **Análises e Relatórios**
- Top 5 categorias com mais chamados
- Top 5 bairros com mais demanda
- Identificar áreas que precisam mais atenção
- Monitorar performance da equipe

✅ **Chamados Recentes**
- Ver últimos chamados criados
- Acompanhar em tempo real
- Clicar para ver detalhes

✅ **Todas as Funcionalidades da Equipe**
- Ver todos os chamados
- Atualizar status
- Filtrar e buscar
- Gerenciar atendimentos

### Interface do Gestor:
- 📞 **Chamados** - Ver TODOS os chamados
- ➕ **Novo Chamado** - Criar chamado
- ✅ **Dashboard** - TEM acesso completo

---

## 🎨 DIFERENÇAS VISUAIS

### Identificação Visual
Cada perfil é identificado com um emoji no header:
- 👤 = Cidadão
- 👷 = Equipe
- 📊 = Gestor
- 🔧 = Admin

### Navegação
- **Cidadão:** 2 abas (Chamados, Novo)
- **Equipe:** 2 abas (Chamados, Novo)
- **Gestor:** 3 abas (Chamados, Novo, Dashboard)

### Títulos
- **Cidadão:** "Meus Chamados"
- **Equipe:** "Todos os Chamados"
- **Gestor:** "Todos os Chamados"

---

## 📋 FLUXO COMPLETO

### 1. Cidadão Reporta Problema
```
1. Cidadão faz login
2. Clica em "Novo Chamado"
3. Preenche formulário com:
   - Título do problema
   - Descrição detalhada
   - Endereço
   - Categoria (ex: Buraco na Via)
   - Bairro
   - Foto (opcional)
4. Envia chamado
5. Recebe protocolo (ex: ZEL-2025-001)
6. Pode acompanhar status em "Meus Chamados"
```

### 2. Equipe Atende Chamado
```
1. Equipe faz login
2. Vai em "Chamados"
3. Vê TODOS os chamados da cidade
4. Filtra por "Aberto" e "Crítica"
5. Clica no chamado
6. Atualiza status para "Em Andamento"
7. Vai ao local e resolve o problema
8. Adiciona foto do serviço concluído
9. Atualiza status para "Resolvido"
```

### 3. Cidadão Avalia
```
1. Cidadão recebe notificação (futuro)
2. Vê que chamado foi resolvido
3. Clica no chamado
4. Vê opção "Avaliar Atendimento"
5. Dá nota de 1 a 5 estrelas
6. Deixa comentário (opcional)
7. Envia avaliação
```

### 4. Gestor Monitora
```
1. Gestor faz login
2. Vai em "Dashboard"
3. Vê estatísticas em tempo real
4. Identifica categoria com mais chamados
5. Vê bairros que precisam mais atenção
6. Analisa avaliação média do serviço
7. Toma decisões baseadas em dados
```

---

## 🚀 TESTANDO AS FUNCIONALIDADES

### Teste como Cidadão
```
Email: pedro.almeida@email.com
Senha: senha123

1. Crie um novo chamado
2. Veja que só aparecem seus chamados
3. Tente avaliar um chamado resolvido
```

### Teste como Equipe
```
Email: joao.silva@belem.pa.gov.br
Senha: senha123

1. Veja que aparecem TODOS os chamados
2. Clique em um chamado
3. Altere o status
4. Veja a mudança ser aplicada
```

### Teste como Gestor
```
Email: maria.santos@belem.pa.gov.br
Senha: senha123

1. Acesse o Dashboard
2. Veja as estatísticas
3. Explore os gráficos
4. Clique em um chamado recente
```

---

## 🎉 PRONTO PARA USAR!

Todas as funcionalidades estão implementadas e funcionando!

**Recarregue a página (CTRL+SHIFT+R) e comece a testar!** 🚀

**Local:** http://localhost:8001/app

---

**Data:** 18/10/2025
**Versão:** 1.0.0
**Sistema:** Zeladoria Urbana - Belém/PA 🏛️
