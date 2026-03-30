# 🏛️ Zelô — Zeladoria Urbana de Belém/PA

> **Versão 4.0.0** | Preparado para a COP 30 | 16 sprints implementadas

Plataforma integrada de zeladoria urbana municipal para a cidade de Belém do Pará.  
Conecta cidadãos, equipes de campo, secretarias e gestores em uma única solução.

---

## 🚀 Início rápido

```bash
# Windows
COMECE_AQUI.bat

# Linux/Mac
cd python-zeladoria
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python seed.py
uvicorn main:app --port 8001 --reload
```

**URLs locais:**
- App: http://localhost:8001/app
- Landing: http://localhost:8001/landing  
- Painel TV: http://localhost:8001/tv
- Docs API: http://localhost:8001/docs

**Logins de teste** (senha: `senha123`):

| Perfil | E-mail |
|--------|--------|
| Admin | admin@belem.pa.gov.br |
| Gestor | maria.santos@belem.pa.gov.br |
| Secretaria | carlos.mendes@seurb.belem.pa.gov.br |
| Equipe | joao.silva@belem.pa.gov.br |
| Cidadão | pedro.almeida@email.com |

---

## 🛠️ Stack

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.11 · FastAPI 0.104 · SQLAlchemy 2.0 |
| Banco (dev) | SQLite |
| Banco (prod) | PostgreSQL + PostGIS |
| Cache | Redis |
| Scheduler | APScheduler 3.10 |
| Frontend | HTML5 · Tailwind-like CSS · Leaflet.js |
| PWA | Service Worker · Web Push · Manifest |
| CI/CD | GitHub Actions |
| Deploy | Railway (Docker) |
| Monitoramento | Sentry |

---

## 📋 Sprints implementadas

### Sprints 1–4 — Fundação & Engajamento
- ✅ Seed idempotente · PostgreSQL robusto
- ✅ PWA (manifest + service worker + offline)
- ✅ Votação em chamados (upvote/toggle)
- ✅ Gamificação (pontos, níveis, conquistas)
- ✅ Abertura de chamado por voz (Web Speech API)

### Sprints 5–8 — Integrações & Transparência
- ✅ Sensores IoT com abertura automática de chamados
- ✅ Webhook WhatsApp Business
- ✅ API pública anonimizada (`/api/publico/`)
- ✅ Orçamento participativo com votação
- ✅ Auditoria blockchain-like (SHA-256 encadeado)
- ✅ Gestão de contratos e fornecedores com nota automática
- ✅ LGPD (exportar/anonimizar/excluir dados)
- ✅ Scheduler SLA + Sentry + CI/CD

### Sprints 9–12 — Geoespacial & IA
- ✅ Mapa de calor em tempo real
- ✅ Clustering DBSCAN + Ordens de Serviço
- ✅ Rastreamento GPS de equipes
- ✅ Score de saúde urbana por bairro
- ✅ Alertas climáticos (OpenWeatherMap)
- ✅ Triagem automática por IA (regras + log de acurácia)
- ✅ Análise de foto
- ✅ Previsão de demanda MA4 por bairro
- ✅ Relatório mensal estruturado
- ✅ Painel público em tempo real

### Sprints 13–16 — COP 30, Testes & Polimento
- ✅ Nheengatu (4º idioma — Língua Geral Amazônica)
- ✅ SSO com Portal Municipal (OAuth2/OIDC + simulação)
- ✅ Painel TV dedicado (`/tv`) para telões públicos
- ✅ Suite de testes pytest (29+ testes)
- ✅ 18 índices PostgreSQL de performance (criados no startup)
- ✅ Push Notifications (Web Push + VAPID)
- ✅ Backup automático diário (SQLite/PostgreSQL)
- ✅ Relatório mensal automático (Cron job — dia 1, 02:00)
- ✅ Limpeza GPS automática (LGPD — dados > 7 dias)
- ✅ Onboarding modal para novos cidadãos
- ✅ Sidebar dinâmica por perfil (5 perfis distintos)
- ✅ Versão 4.0.0

---

## 🎭 Perfis de usuário

| Perfil | Acesso |
|--------|--------|
| **Cidadão** | Chamados próprios, novo chamado, perfil/gamificação, ranking, propostas |
| **Equipe** | Chamados atribuídos, ordens de serviço, GPS, mapa |
| **Secretaria** | Chamados da secretaria, painel SLA, dashboard, triagem IA |
| **Gestor** | Tudo + equipes no campo, clusters, previsão, relatórios |
| **Admin** | Tudo + usuários, sensores IoT, contratos, auditoria blockchain |

---

## 🔑 Variáveis de ambiente (Railway)

```env
# Obrigatórias
DATABASE_URL=postgresql://...
SECRET_KEY=<gerar: python -c "import secrets; print(secrets.token_urlsafe(64))">

# Opcionais
SENTRY_DSN=https://...
OPENWEATHER_API_KEY=...
WA_VERIFY_TOKEN=...
WA_ACCESS_TOKEN=...
VAPID_PUBLIC_KEY=...
VAPID_PRIVATE_KEY=...
SSO_PROVIDER_URL=https://keycloak.belem.pa.gov.br/realms/cidadao
SSO_CLIENT_ID=zelo-app
SSO_CLIENT_SECRET=...
POPULATE_DATA=true  # apenas no primeiro deploy
```

---

## 🧪 Testes

```bash
cd python-zeladoria
pytest tests/ -v --tb=short
```

Cobertura: auth, chamados, API pública, engajamento, IA, health.

---

## 🐳 Docker

```bash
# Build e run local
docker build -t zelo-backend ./python-zeladoria
docker run -p 8001:8001 -e SECRET_KEY=dev-key zelo-backend

# Com docker-compose (banco + redis incluídos)
docker-compose up -d
```

---

## 📡 Endpoints principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/publico/estatisticas` | Estatísticas públicas |
| GET | `/api/publico/chamados` | Chamados anonimizados |
| GET | `/api/ia/painel-publico` | Dados para telão |
| GET | `/api/geo/heatmap` | Mapa de calor |
| POST | `/api/ia/triar` | Triagem por IA |
| GET | `/api/sso/iniciar` | Login via Portal Municipal |
| GET | `/tv` | Painel TV público |
| GET | `/landing` | Landing page |
| GET | `/docs` | Swagger UI |

---

## 🌿 Idiomas suportados

- 🇧🇷 Português (PT-BR)
- 🇺🇸 English (EN)
- 🇪🇸 Español (ES)  
- 🌿 Nheengatu (NHE) — Língua Geral Amazônica

---

*Zelô — Zeladoria Urbana de Belém/PA · Prefeitura Municipal · COP 30 · 2025*
