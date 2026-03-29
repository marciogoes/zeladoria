# ✅ CHECKLIST DE DEPLOY - PRODUÇÃO

## 🚀 PREPARAÇÃO PARA PRODUÇÃO

**Sistema:** Dashboard de Zeladoria Urbana - Belém/PA  
**Versão:** 2.0.0  
**Data:** ___/___/2025

---

## 📋 PRÉ-REQUISITOS

### **Infraestrutura**
- [ ] Servidor Linux/Windows preparado
- [ ] Domínio configurado
- [ ] SSL/HTTPS configurado
- [ ] Firewall configurado
- [ ] Backup automatizado configurado

### **Software**
- [ ] Python 3.8+ instalado
- [ ] Banco de dados em produção (PostgreSQL/MySQL)
- [ ] Nginx/Apache configurado
- [ ] Supervisor/systemd configurado
- [ ] Git instalado

---

## 🔧 CONFIGURAÇÃO DO BACKEND

### **1. Ambiente Virtual**
```bash
- [ ] python -m venv venv
- [ ] source venv/bin/activate  # Linux
- [ ] venv\Scripts\activate      # Windows
- [ ] pip install -r requirements.txt
```

### **2. Variáveis de Ambiente**
```bash
- [ ] Criar arquivo .env
- [ ] DATABASE_URL=postgresql://...
- [ ] SECRET_KEY=<chave-forte-aleatória>
- [ ] API_URL=https://seu-dominio.com
- [ ] ENVIRONMENT=production
- [ ] DEBUG=False
```

### **3. Banco de Dados**
```bash
- [ ] Criar banco de produção
- [ ] Executar migrações
- [ ] Importar dados iniciais
- [ ] Configurar backup automático
- [ ] Testar conexão
```

### **4. Arquivos Estáticos**
```bash
- [ ] Copiar /frontend para /var/www/zeladoria
- [ ] Configurar permissões (chmod 755)
- [ ] Verificar todos os arquivos presentes:
      - [ ] index.html
      - [ ] app.js
      - [ ] dashboard.js
      - [ ] dashboard-advanced.js
      - [ ] style.css (se existir)
```

---

## 🌐 CONFIGURAÇÃO DO FRONTEND

### **1. URLs da API**
```javascript
- [ ] Atualizar app.js:
      const API_URL = 'https://api.seu-dominio.com';
- [ ] Testar endpoints
- [ ] Verificar CORS
```

### **2. Chart.js e Dependências**
```html
- [ ] Verificar CDN do Chart.js carregando
- [ ] Verificar Leaflet.js carregando
- [ ] Testar em diferentes navegadores
```

### **3. Otimização**
```bash
- [ ] Minificar JavaScript
- [ ] Minificar CSS
- [ ] Otimizar imagens
- [ ] Configurar cache do navegador
```

---

## 🔐 SEGURANÇA

### **1. Autenticação**
```bash
- [ ] Alterar senhas padrão
- [ ] Gerar SECRET_KEY forte
- [ ] Configurar JWT com expiração
- [ ] Implementar rate limiting
- [ ] Habilitar 2FA (opcional)
```

### **2. HTTPS**
```bash
- [ ] Certificado SSL instalado
- [ ] Redirecionar HTTP → HTTPS
- [ ] Configurar HSTS
- [ ] Testar em SSL Labs
```

### **3. Proteção**
```bash
- [ ] Configurar firewall (porta 80, 443)
- [ ] Bloquear acessos diretos ao backend
- [ ] Configurar WAF (opcional)
- [ ] Implementar logging de segurança
```

### **4. Dados Sensíveis**
```bash
- [ ] Remover dados de teste
- [ ] Remover credenciais de desenvolvimento
- [ ] Configurar backup criptografado
```

---

## 🖥️ SERVIDOR WEB

### **Nginx (Recomendado)**
```nginx
- [ ] Criar arquivo /etc/nginx/sites-available/zeladoria
- [ ] Configurar proxy_pass para FastAPI
- [ ] Configurar servir arquivos estáticos
- [ ] Configurar gzip
- [ ] Configurar cache
- [ ] Testar configuração: nginx -t
- [ ] Reiniciar: systemctl restart nginx
```

**Exemplo de Configuração:**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

    # Frontend
    location / {
        root /var/www/zeladoria/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Arquivos estáticos
    location /static {
        alias /var/www/zeladoria/frontend;
        expires 30d;
    }
}
```

---

## 🔄 SUPERVISOR/SYSTEMD

### **Supervisor (FastAPI)**
```ini
- [ ] Criar /etc/supervisor/conf.d/zeladoria.conf
```

**Configuração:**
```ini
[program:zeladoria]
command=/home/user/zeladoria/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
directory=/home/user/zeladoria/python-zeladoria
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/zeladoria/app.log
```

```bash
- [ ] supervisorctl reread
- [ ] supervisorctl update
- [ ] supervisorctl start zeladoria
- [ ] supervisorctl status
```

### **Systemd (Alternativa)**
```bash
- [ ] Criar /etc/systemd/system/zeladoria.service
- [ ] systemctl daemon-reload
- [ ] systemctl enable zeladoria
- [ ] systemctl start zeladoria
- [ ] systemctl status zeladoria
```

---

## 📊 MONITORAMENTO

### **Logs**
```bash
- [ ] Configurar rotação de logs
- [ ] Configurar nível de log (INFO em prod)
- [ ] Monitorar erros 500
- [ ] Alertas para erros críticos
```

**Locais dos Logs:**
```bash
- [ ] /var/log/zeladoria/app.log
- [ ] /var/log/nginx/access.log
- [ ] /var/log/nginx/error.log
```

### **Métricas**
```bash
- [ ] Monitorar CPU
- [ ] Monitorar RAM
- [ ] Monitorar Disco
- [ ] Monitorar Rede
- [ ] Monitorar Tempo de Resposta
```

### **Ferramentas (Opcional)**
```bash
- [ ] Prometheus
- [ ] Grafana
- [ ] New Relic
- [ ] Datadog
- [ ] Sentry (erros)
```

---

## 🧪 TESTES EM PRODUÇÃO

### **1. Testes Funcionais**
```bash
- [ ] Login funciona
- [ ] Dashboard carrega
- [ ] Todas as 5 tabs navegam
- [ ] Gráficos renderizam
- [ ] Exportação CSV funciona
- [ ] Comparação de períodos funciona
- [ ] Alertas aparecem
- [ ] Filtros funcionam
```

### **2. Testes de Performance**
```bash
- [ ] Tempo de carregamento < 3s
- [ ] Teste de carga (1000 usuários)
- [ ] Teste de stress
- [ ] Verificar memory leaks
```

### **3. Testes de Segurança**
```bash
- [ ] SQL Injection
- [ ] XSS
- [ ] CSRF
- [ ] Brute Force
- [ ] Scan de vulnerabilidades
```

### **4. Testes de Compatibilidade**
```bash
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile (Android)
- [ ] Mobile (iOS)
```

---

## 💾 BACKUP

### **Configuração**
```bash
- [ ] Backup diário do banco
- [ ] Backup semanal completo
- [ ] Retenção: 30 dias
- [ ] Backup offsite (AWS S3, etc)
- [ ] Testar restauração
```

**Script de Backup:**
```bash
#!/bin/bash
- [ ] Criar /opt/scripts/backup-zeladoria.sh
- [ ] Adicionar ao cron: 0 2 * * * /opt/scripts/backup-zeladoria.sh
```

---

## 📧 NOTIFICAÇÕES

### **Alertas**
```bash
- [ ] Email para erros críticos
- [ ] Email para SLA < 80%
- [ ] Email para backup falho
- [ ] SMS para downtime (opcional)
```

### **Relatórios**
```bash
- [ ] Relatório diário de uso
- [ ] Relatório semanal de métricas
- [ ] Relatório mensal executivo
```

---

## 👥 USUÁRIOS

### **Criação**
```bash
- [ ] Criar usuário admin
- [ ] Criar usuários gestores
- [ ] Criar usuários equipe
- [ ] Remover usuários de teste
- [ ] Definir senhas fortes
```

### **Permissões**
```bash
- [ ] Admin: acesso total
- [ ] Gestor: dashboard + relatórios
- [ ] Equipe: chamados
- [ ] Cidadão: criar e acompanhar
```

---

## 📖 DOCUMENTAÇÃO

### **Para Usuários**
```bash
- [ ] Manual do usuário
- [ ] Vídeo tutorial
- [ ] FAQ
- [ ] Suporte: email/telefone
```

### **Para Equipe Técnica**
```bash
- [ ] Documentação da API
- [ ] Procedimentos de deploy
- [ ] Troubleshooting
- [ ] Contatos de emergência
```

---

## 🎓 TREINAMENTO

### **Gestores**
```bash
- [ ] Treinamento de 2h sobre o dashboard
- [ ] Como gerar relatórios
- [ ] Como interpretar métricas
- [ ] Como usar alertas
```

### **Equipe Operacional**
```bash
- [ ] Treinamento de 1h sobre chamados
- [ ] Como atualizar status
- [ ] Como usar o mapa
- [ ] Como avaliar
```

### **Suporte Técnico**
```bash
- [ ] Procedimentos de backup/restore
- [ ] Como monitorar logs
- [ ] Como resolver problemas comuns
- [ ] Contatos de escalação
```

---

## 🚨 PLANO DE CONTINGÊNCIA

### **Downtime**
```bash
- [ ] Página de manutenção pronta
- [ ] Procedimento de rollback
- [ ] Contatos de emergência
- [ ] Comunicação com usuários
```

### **Disaster Recovery**
```bash
- [ ] Backup offsite testado
- [ ] Servidor de backup (opcional)
- [ ] RTO definido (tempo máximo de recuperação)
- [ ] RPO definido (perda máxima de dados)
```

---

## ✅ CHECKLIST FINAL DE PRODUÇÃO

### **Dia do Deploy**
```bash
- [ ] 08:00 - Backup completo
- [ ] 09:00 - Deploy do backend
- [ ] 09:30 - Deploy do frontend
- [ ] 10:00 - Testes funcionais
- [ ] 10:30 - Testes de performance
- [ ] 11:00 - Smoke tests
- [ ] 11:30 - Treinamento final da equipe
- [ ] 12:00 - Sistema em produção
- [ ] 12:30 - Monitoramento ativo
- [ ] 18:00 - Revisão do primeiro dia
```

### **Primeira Semana**
```bash
- [ ] Dia 1: Monitoramento intensivo
- [ ] Dia 2: Ajustes de performance
- [ ] Dia 3: Feedback dos usuários
- [ ] Dia 4: Correções necessárias
- [ ] Dia 5: Estabilização
- [ ] Dia 7: Revisão completa
```

---

## 📊 MÉTRICAS DE SUCESSO

### **Técnicas**
```bash
- [ ] Uptime > 99.5%
- [ ] Tempo de resposta < 2s
- [ ] Zero erros críticos
- [ ] Backup 100% OK
```

### **Negócio**
```bash
- [ ] 100% dos gestores treinados
- [ ] 95% de satisfação dos usuários
- [ ] Redução de 30% no tempo de resolução
- [ ] Aumento de 50% na transparência
```

---

## 🎉 PÓS-DEPLOY

### **Primeira Semana**
```bash
- [ ] Coletar feedback
- [ ] Ajustar configurações
- [ ] Corrigir bugs menores
- [ ] Otimizar performance
```

### **Primeiro Mês**
```bash
- [ ] Análise completa de uso
- [ ] Relatório de métricas
- [ ] Planejamento de melhorias
- [ ] Versão 2.1 (roadmap)
```

---

## 📞 CONTATOS DE EMERGÊNCIA

```
Desenvolvedor Backend:  _________________
Desenvolvedor Frontend: _________________
DBA:                    _________________
Infraestrutura:         _________________
Gestor do Projeto:      _________________
Suporte 24/7:           _________________
```

---

## 📝 ASSINATURAS

```
Deploy realizado por:    _________________ Data: ___/___/___
Aprovado por (Técnico):  _________________ Data: ___/___/___
Aprovado por (Gestor):   _________________ Data: ___/___/___
Homologado por:          _________________ Data: ___/___/___
```

---

## 🎊 CONCLUSÃO

```
╔═══════════════════════════════════════════════╗
║                                               ║
║   SISTEMA PRONTO PARA PRODUÇÃO!              ║
║                                               ║
║   ✅ Todos os itens verificados              ║
║   ✅ Testes realizados                       ║
║   ✅ Equipe treinada                         ║
║   ✅ Backup configurado                      ║
║   ✅ Monitoramento ativo                     ║
║                                               ║
║        🚀 BOA SORTE NO DEPLOY! 🚀           ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

**Sistema de Zeladoria Urbana - Belém/PA**  
**Checklist de Deploy para Produção**  
**Versão:** 2.0.0  
**Data:** 18 de Outubro de 2025
