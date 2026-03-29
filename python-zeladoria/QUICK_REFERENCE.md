# 🎯 CARD DE REFERÊNCIA RÁPIDA - DASHBOARD

## ⚡ ACESSO RÁPIDO

### **🔐 Login**
```
Email: maria.santos@belem.pa.gov.br
Senha: senha123
Menu: 📊 Dashboard
```

### **🖥️ URL**
```
http://localhost:8001/static/index.html
```

---

## 📊 5 TABS PRINCIPAIS

### **🏠 VISÃO GERAL**
```
• 8 KPIs principais
• Top 5 Categorias
• Top 5 Bairros
• Chamados recentes
```

### **📊 ANÁLISES**
```
• Status
• Prioridade
• Região
• Temporal
• Avaliações
• Categorias críticas
```

### **👥 EQUIPE**
```
• Ranking (🥇🥈🥉)
• Carga de trabalho
• Produtividade
```

### **⏱️ SLA & TEMPO**
```
• SLA cumprido
• Tempo médio
• Vencendo hoje
• Vencidos
```

### **📝 RELATÓRIOS**
```
• Gerar
• Exportar CSV
• Imprimir
• Comparar períodos
```

---

## 🔔 ALERTAS AUTOMÁTICOS

```
🚨 SLA < 80%        → Crítico
⚠️ Vencidos > 10    → Atenção
⚠️ Avaliação < 4.0  → Atenção
💡 Andamento > 50   → Info
```

---

## 🗓️ FILTROS DE DATA

```
✅ Hoje
✅ Esta Semana
✅ Este Mês
✅ Este Trimestre
✅ Este Ano
✅ Personalizado
```

---

## 📈 GRÁFICOS CHART.JS

```
🥧 Pizza      → Status
📈 Linha      → Temporal (30d)
📊 Barras     → Categorias
```

---

## 💾 EXPORTAR

```
Botão: 💾 Exportar CSV
• Cabeçalho completo
• Metadados
• UTF-8 encoding
• Nome automático
```

---

## 📊 COMPARAR PERÍODOS

```
Botão: 📊 Comparar Períodos
• Atual vs Anterior
• Variações %
• Insights automáticos
```

---

## ⌨️ ATALHOS

| Ação | Como |
|------|------|
| Login Gestor | Click "📊 Gestor" |
| Abrir Dashboard | Click "📊 Dashboard" |
| Trocar Tab | Click no nome da tab |
| Ver Chamado | Click no chamado |
| Exportar | Click "💾 Exportar CSV" |
| Comparar | Click "📊 Comparar" |

---

## 🎨 CORES

```css
🔵 Azul     → Primary (#1e40af)
🟢 Verde    → Success (#10b981)
🟡 Amarelo  → Warning (#f59e0b)
🔴 Vermelho → Danger (#ef4444)
```

---

## 📱 RESPONSIVO

```
Desktop  → 4 colunas
Tablet   → 2 colunas
Mobile   → 1 coluna
```

---

## 🐛 TROUBLESHOOTING

| Problema | Solução |
|----------|---------|
| Dashboard não carrega | Verificar backend rodando |
| Sem dados | Executar `python seed.py` |
| Tabs não navegam | Verificar `dashboard.js` |
| Gráficos não aparecem | Login como Gestor |

---

## 📁 ARQUIVOS PRINCIPAIS

```
/frontend/
├── index.html
├── app.js
├── dashboard.js
└── dashboard-advanced.js

/
├── DASHBOARD_IMPLEMENTADO.md
├── GUIA_RAPIDO_DASHBOARD.md
├── RESUMO_VISUAL_DASHBOARD.md
├── FUNCIONALIDADES_AVANCADAS.md
└── RESUMO_CONSOLIDADO.md
```

---

## ✅ CHECKLIST RÁPIDO

```
□ Backend rodando
□ Navegador aberto
□ Login como gestor
□ Dashboard acessível
□ 5 tabs funcionando
□ Gráficos carregando
□ Alertas visíveis
□ Exportação OK
```

---

## 🎯 MÉTRICAS PRINCIPAIS

| KPI | Fórmula |
|-----|---------|
| Taxa Resolução | (Resolvidos / Total) × 100 |
| SLA | (No prazo / Total) × 100 |
| Tempo Médio | Σ tempos / Quantidade |

---

## 🚀 COMANDOS ÚTEIS

```bash
# Iniciar backend
cd python-zeladoria
python main.py

# Popular dados
python seed.py

# Verificar logs
tail -f logs/app.log
```

---

## 📞 SUPORTE

**Problema com login?**
→ Usar botão "📊 Gestor"

**Problema com dados?**
→ Executar seed.py

**Problema com gráficos?**
→ Verificar Chart.js carregado

**Problema com tabs?**
→ F12 → Console → Ver erros

---

## 💡 DICAS

✅ Use "Comparar Períodos" para análises
✅ Monitore alertas na Visão Geral
✅ Exporte dados regularmente
✅ Verifique SLA diariamente
✅ Acompanhe ranking da equipe

---

## 🎊 VERSÃO

```
Dashboard: 2.0.0
Data: 18/10/2025
Status: ✅ PRONTO
```

---

**Sistema de Zeladoria Urbana - Belém/PA**
**Card de Referência Rápida**
