# 📋 Catálogo de Serviços - Sistema de Zeladoria Urbana

## 🎯 Visão Geral

Sistema de catálogo de serviços públicos com **SLA (Service Level Agreement)** definido para cada tipo de atendimento. Cada secretaria gerencia seu próprio catálogo de serviços.

## 📊 Estatísticas

- **100+ serviços** cadastrados
- **5 secretarias** principais
- **SLAs** de 4h até 90 dias
- **Prioridades** de Emergencial a Agendável

## 🏢 Secretarias Cobertas

### 1. SEURB - Secretaria de Urbanismo (17 serviços)
- Iluminação Pública (4 serviços)
- Pavimentação e Vias (4 serviços)
- Calçadas (2 serviços)
- Sinalização (3 serviços)
- Praças e Parques (3 serviços)

### 2. SESAN - Secretaria de Saneamento (12 serviços)
- Coleta de Resíduos (3 serviços)
- Limpeza Urbana (3 serviços)
- Varrição (2 serviços)
- Drenagem (2 serviços)
- Cemitérios (2 serviços)

### 3. SEMOB - Secretaria de Mobilidade (18 serviços)
- Transporte Público (6 serviços)
- Pontos de Ônibus (2 serviços)
- Semáforos (3 serviços)
- Estacionamento (3 serviços)
- Ciclovias (2 serviços)

### 4. SEMMA - Secretaria de Meio Ambiente (22 serviços)
- Arborização (6 serviços)
- Denúncias Ambientais (5 serviços)
- Animais (3 serviços)
- Licenciamento (2 serviços)
- Educação Ambiental (2 serviços)

### 5. SESMA - Secretaria de Saúde (13 serviços)
- Vigilância Sanitária (3 serviços)
- Controle de Vetores (4 serviços)
- Zoonoses (3 serviços)
- Vigilância Epidemiológica (1 serviço)

## ⚡ Níveis de Prioridade

### 🚨 Emergencial (< 12h)
Situações que apresentam risco imediato à segurança ou saúde pública.

**Exemplos:**
- Iluminação pública em emergência (12h)
- Remoção de árvore caída (8h)
- Reparo emergencial em via (8h)
- Controle de animais peçonhentos (8h)
- Atendimento a acidente com animal (4h)
- Limpeza emergencial de bueiro (4h)

### 🔴 Alta (12-24h)
Problemas graves que precisam de resolução rápida.

**Exemplos:**
- Reparo de poste de iluminação (48h)
- Tapa-buraco em via pública (96h)
- Limpeza de boca de lobo (48h)
- Coleta de lixo não realizada (24h)
- Poda de árvore em emergência (12h)

### 🟡 Média (24-72h)
Serviços regulares com prazo intermediário.

**Exemplos:**
- Troca de lâmpada pública (72h)
- Varrição de via pública (48h)
- Reparo de calçada pública (240h)
- Poda de árvore (240h)
- Cartão de transporte estudantil (240h)

### 🟢 Baixa (> 72h)
Projetos de longo prazo ou melhorias não urgentes.

**Exemplos:**
- Recapeamento de via (1440h / 60 dias)
- Pavimentação de via não asfaltada (2160h / 90 dias)
- Construção de nova galeria (1440h / 60 dias)
- Licença ambiental completa (2160h / 90 dias)

### 📅 Agendável
Serviços que podem ser programados conforme disponibilidade.

**Exemplos:**
- Revitalização de praça
- Palestra de educação ambiental
- Visita técnica ambiental
- Vacinação antirrábica (conforme campanhas)

## 💰 Custos

A maioria dos serviços é **gratuita** (91 de 100+). Alguns serviços cobram taxas:

**Serviços Pagos:**
- Concessão de túmulo: R$ 150,00
- Cartão de transporte estudantil: R$ 15,00
- Autorização para poda em área particular: R$ 80,00
- Autorização para corte de árvore: R$ 150,00
- Licença ambiental simplificada: R$ 250,00
- Licença ambiental completa: R$ 1.500,00
- Alvará sanitário: R$ 300,00

## 🔧 Como Popular o Banco

### Pré-requisitos
1. Banco de dados configurado
2. Secretarias já cadastradas no sistema
3. IDs das secretarias conhecidos

### Executar o Seed

```bash
# Método 1: Executar diretamente
cd app/seeds
python seed_servicos.py

# Método 2: Via script de gestão
python manage_catalogo.py seed

# Método 3: Via Python
from app.seeds import seed_servicos
seed_servicos()
```

### Ajustar IDs das Secretarias

No arquivo `seed_servicos.py`, ajuste o mapeamento conforme seu banco:

```python
secretarias_map = {
    "SEURB": 1,   # ID da SEURB no seu banco
    "SESAN": 2,   # ID da SESAN no seu banco
    "SEMOB": 3,   # ID da SEMOB no seu banco
    "SEMMA": 4,   # ID da SEMMA no seu banco
    "SESMA": 5,   # ID da SESMA no seu banco
}
```

## 📝 Estrutura do Modelo

```python
class ServicoSecretaria(Base):
    # Identificação
    codigo: str              # Ex: SEURB-001
    nome: str                # Nome do serviço
    descricao: str           # Descrição detalhada
    categoria: str           # Categoria principal
    subcategoria: str        # Subcategoria específica
    
    # SLA
    sla_horas: int           # Tempo de atendimento (horas)
    prioridade: enum         # emergencial/alta/media/baixa/agendavel
    
    # Atendimento
    documentos_necessarios   # Documentos requeridos
    custo: float             # Custo em R$ (0 = gratuito)
    requisitos: str          # Requisitos técnicos
    
    # Canais
    atendimento_presencial   # Permite presencial?
    atendimento_online       # Permite online?
    atendimento_telefone     # Permite telefone?
    
    # Métricas
    total_solicitacoes       # Total de chamados
    taxa_cumprimento_sla     # % de cumprimento
    avaliacao_media          # Nota média (1-5)
```

## 🎨 Properties Úteis

```python
servico.sla_em_dias          # "48h" ou "2 dia(s)"
servico.prioridade_label     # "🚨 Emergencial"
servico.custo_formatado      # "Gratuito" ou "R$ 150.00"
```

## 📈 Próximos Passos

1. ✅ Modelo de serviços criado
2. ✅ Seed com 100+ serviços realistas
3. ⏳ API endpoints para gestão do catálogo
4. ⏳ Interface administrativa
5. ⏳ Sistema de busca e filtros
6. ⏳ Integração com chamados
7. ⏳ Dashboard de métricas por serviço

## 🔍 Exemplos de Uso

### Buscar serviços por categoria
```python
servicos = db.query(ServicoSecretaria)\
    .filter_by(categoria="Iluminação Pública")\
    .all()
```

### Buscar serviços emergenciais
```python
servicos_urgentes = db.query(ServicoSecretaria)\
    .filter_by(prioridade=PrioridadeServico.EMERGENCIAL)\
    .all()
```

### Buscar serviços gratuitos online
```python
servicos_online = db.query(ServicoSecretaria)\
    .filter_by(
        custo=0.0,
        atendimento_online=True,
        status=StatusServico.ATIVO
    ).all()
```

## 📞 Canais de Atendimento

Cada serviço pode estar disponível em:
- 🏢 **Presencial**: Atendimento nas sedes das secretarias
- 💻 **Online**: Portal web e aplicativo
- ☎️ **Telefone**: Call center 156

## 🎯 KPIs do Catálogo

O sistema rastreia automaticamente:
- **Taxa de cumprimento de SLA**: % de chamados resolvidos no prazo
- **Tempo médio de atendimento**: Tempo real vs SLA prometido
- **Avaliação média**: Satisfação do cidadão (1-5 estrelas)
- **Volume de solicitações**: Quantidade por tipo de serviço

---

**Desenvolvido para**: Sistema de Zeladoria Urbana - Belém/PA 🌴
**Versão**: 1.0
**Data**: Outubro 2025
