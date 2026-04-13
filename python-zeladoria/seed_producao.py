"""
seed_producao.py v2 — Robusto, com retry e rate-limit handling
Execute: python seed_producao.py
"""
import requests, random, time
from datetime import datetime, timedelta

BASE = "https://zeladoria-backend-production.up.railway.app/api"
H    = {"Content-Type": "application/json"}
token = None

def ok(m):  print(f"  ✅ {m}")
def err(m): print(f"  ❌ {m}")
def log(m): print(f"  ⏳ {m}")

def login(email, senha):
    r = requests.post(f"{BASE}/auth/login", json={"email": email, "senha": senha}, headers=H, timeout=15)
    if r.ok:
        data = r.json()
        return data.get("access_token") or data.get("token")
    return None

def api(method, endpoint, data=None, tok=None):
    t = tok or token
    h = {**H, "Authorization": f"Bearer {t}"} if t else H
    fn = {"GET": requests.get, "POST": requests.post, "PATCH": requests.patch}[method]
    kwargs = {"headers": h, "timeout": 15}
    if data is not None:
        kwargs["json"] = data
    try:
        return fn(f"{BASE}{endpoint}", **kwargs)
    except Exception as e:
        print(f"  ⚠️  {e}")
        return None

def registrar(u):
    """Registra usuário, aguarda se rate-limited."""
    for tentativa in range(3):
        r = requests.post(f"{BASE}/auth/register", json=u, headers=H, timeout=15)
        if r.status_code == 429:
            log(f"Rate limit — aguardando 10s ({u['email']})")
            time.sleep(10)
            continue
        if r.status_code in (200, 201):
            ok(f"Criado: {u['email']}")
            return True
        if r.status_code == 400 and "already" in r.text.lower():
            log(f"Já existe: {u['email']}")
            return True
        log(f"{u['email']} → {r.status_code}: {r.text[:60]}")
        return True
    return False

# ══════════════════════════════════════════════════════════════════
# 1. USUÁRIOS
# ══════════════════════════════════════════════════════════════════
print("\n👥 Criando usuários (com pausa anti-rate-limit)...")

USUARIOS = [
    {"nome": "Admin Sistema",         "email": "admin@zeladoria.com",   "senha": "admin123",   "tipo": "admin"},
    {"nome": "Gestor Municipal",       "email": "gestor@zeladoria.com",  "senha": "gestor123",  "tipo": "gestor"},
    {"nome": "Equipe Campo A",         "email": "equipe@zeladoria.com",  "senha": "equipe123",  "tipo": "equipe"},
    {"nome": "Equipe Campo B",         "email": "equipe2@zeladoria.com", "senha": "equipe123",  "tipo": "equipe"},
    {"nome": "Cidadão João",           "email": "cidadao@zeladoria.com", "senha": "cidadao123", "tipo": "cidadao"},
    {"nome": "Maria Silva",            "email": "maria@zeladoria.com",   "senha": "cidadao123", "tipo": "cidadao"},
    {"nome": "Carlos Oliveira",        "email": "carlos@zeladoria.com",  "senha": "cidadao123", "tipo": "cidadao"},
    {"nome": "Ana Costa SEURB",        "email": "seurb@zeladoria.com",   "senha": "seurb123",   "tipo": "secretaria"},
    {"nome": "Pedro Santos SESAN",     "email": "sesan@zeladoria.com",   "senha": "sesan123",   "tipo": "secretaria"},
    {"nome": "Luiza Ferreira SEMOB",   "email": "semob@zeladoria.com",   "senha": "semob123",   "tipo": "secretaria"},
    {"nome": "Roberto Lima SEMMA",     "email": "semma@zeladoria.com",   "senha": "semma123",   "tipo": "secretaria"},
    {"nome": "Fatima Souza SESMA",     "email": "sesma@zeladoria.com",   "senha": "sesma123",   "tipo": "secretaria"},
]

for u in USUARIOS:
    registrar(u)
    time.sleep(2)   # pausa entre registros para evitar 429

# ══════════════════════════════════════════════════════════════════
# 2. LOGIN ADMIN
# ══════════════════════════════════════════════════════════════════
print("\n🔑 Login admin...")
token = login("admin@zeladoria.com", "admin123")
if not token:
    print("❌ Falha no login. Verifique se o usuário admin foi criado.")
    exit(1)
ok("Login OK")

# ══════════════════════════════════════════════════════════════════
# 3. CATEGORIAS E BAIRROS
# ══════════════════════════════════════════════════════════════════
r = api("GET", "/categorias")
cat_ids = [c["id"] for c in r.json()] if r and r.ok else []
ok(f"{len(cat_ids)} categorias")

r = api("GET", "/bairros")
bairro_ids = [b["id"] for b in r.json()] if r and r.ok else []
ok(f"{len(bairro_ids)} bairros")

# ══════════════════════════════════════════════════════════════════
# 4. CHAMADOS (usando token admin — mais estável)
# ══════════════════════════════════════════════════════════════════
print("\n📋 Criando 30 chamados...")

TITULOS = [
    ("Buraco profundo na calçada prejudica pedestres",      "baixa"),
    ("Iluminação pública apagada há 3 semanas",             "media"),
    ("Lixo acumulado próximo à escola municipal",           "alta"),
    ("Árvore caída bloqueando via principal",               "critica"),
    ("Vazamento de esgoto na rua principal",                "alta"),
    ("Calçada danificada por raízes de árvore",            "baixa"),
    ("Poda urgente de árvore sobre fiação elétrica",       "critica"),
    ("Bueiro entupido causando alagamento",                 "alta"),
    ("Placa de trânsito danificada na rotatória",          "media"),
    ("Faixa de pedestre apagada em via movimentada",       "media"),
    ("Lâmpada queimada na praça da comunidade",            "baixa"),
    ("Entulho irregular depositado em área pública",       "media"),
    ("Buraco na pista causa acidentes frequentes",         "critica"),
    ("Semáforo com defeito no cruzamento central",         "alta"),
    ("Calçamento destruído por obras sem reparo",          "media"),
    ("Alagamento recorrente após chuvas no bairro",        "alta"),
    ("Poste inclinado oferece risco à população",          "critica"),
    ("Lixo em terreno baldio gera foco de dengue",        "alta"),
    ("Meio-fio quebrado dificulta acessibilidade",         "baixa"),
    ("Galeria pluvial obstruída pela vegetação",           "media"),
    ("Praça com brinquedos danificados e enferrujados",    "media"),
    ("Via sem pavimentação dificulta mobilidade",          "baixa"),
    ("Esgoto a céu aberto próximo a residências",         "critica"),
    ("Sinalização viária apagada na saída da cidade",      "media"),
    ("Árvore doente com risco de queda iminente",          "alta"),
    ("Pista com ondulações perigosas para motociclistas",  "media"),
    ("Falta de rampas de acessibilidade na calçada",      "baixa"),
    ("Container de lixo transbordando há dias",            "alta"),
    ("Buraco no meio da avenida sem sinalização",          "critica"),
    ("Mato alto em área pública atraindo animais",        "baixa"),
]

COORDS = [
    (-1.4558, -48.4902), (-1.4780, -48.5001), (-1.4200, -48.4600),
    (-1.4900, -48.4700), (-1.4650, -48.5100), (-1.4450, -48.5200),
    (-1.5000, -48.4800), (-1.4300, -48.4900), (-1.4700, -48.4400),
    (-1.4100, -48.5000),
]

STATUS_CICLO = ["aberto","aberto","aberto","em_andamento","em_andamento","resolvido","cancelado"]
chamado_ids = []

for i, (titulo, prioridade) in enumerate(TITULOS):
    # Renova token admin a cada 10 chamados
    if i % 10 == 0 and i > 0:
        novo = login("admin@zeladoria.com", "admin123")
        if novo:
            token = novo

    lat, lng = random.choice(COORDS)
    payload = {
        "titulo": titulo,
        "descricao": f"Problema identificado pelos moradores: {titulo}. Solicitamos verificação e providências urgentes.",
        "prioridade": prioridade,
        "latitude": round(lat + random.uniform(-0.005, 0.005), 6),
        "longitude": round(lng + random.uniform(-0.005, 0.005), 6),
        "endereco": f"Rua {random.choice(['das Flores','do Sol','da Paz','Principal'])}, {random.randint(100,2000)} - Belém/PA",
    }
    if cat_ids:   payload["categoria_id"] = random.choice(cat_ids)
    if bairro_ids: payload["bairro_id"]   = random.choice(bairro_ids)

    r = api("POST", "/chamados", payload)
    if r and r.ok:
        cid = r.json().get("id")
        chamado_ids.append(cid)
        print(f"  [{i+1:02d}/30] ✅ {titulo[:48]}")
    else:
        code = r.status_code if r else "timeout"
        print(f"  [{i+1:02d}/30] ❌ {code}")
    time.sleep(0.4)

ok(f"{len(chamado_ids)} chamados criados")

# ══════════════════════════════════════════════════════════════════
# 5. STATUS DOS CHAMADOS
# ══════════════════════════════════════════════════════════════════
print("\n🔄 Atualizando status...")
token = login("admin@zeladoria.com", "admin123") or token

for i, cid in enumerate(chamado_ids):
    status = STATUS_CICLO[i % len(STATUS_CICLO)]
    if status != "aberto":
        r = api("PATCH", f"/chamados/{cid}/status", {"status": status})
        time.sleep(0.3)
ok("Status atualizados")

# ══════════════════════════════════════════════════════════════════
# 6. AVALIAÇÕES (chamados resolvidos)
# ══════════════════════════════════════════════════════════════════
print("\n⭐ Avaliando chamados resolvidos...")
tok_cid = login("cidadao@zeladoria.com", "cidadao123")
if tok_cid:
    FRASES = [
        "Ótimo atendimento, problema resolvido rapidamente!",
        "Demorou mas resolveram. Satisfeito.",
        "Excelente serviço da equipe municipal!",
        "Razoável, esperava mais agilidade.",
        "Muito bom! Profissionais competentes.",
    ]
    for i, cid in enumerate(chamado_ids):
        if STATUS_CICLO[i % len(STATUS_CICLO)] == "resolvido":
            api("POST", f"/chamados/{cid}/avaliar", {
                "avaliacao": random.randint(3, 5),
                "comentario_avaliacao": random.choice(FRASES),
            }, tok=tok_cid)
            time.sleep(0.3)
    ok("Avaliações registradas")
else:
    err("Cidadão não encontrado — avaliações puladas")

# ══════════════════════════════════════════════════════════════════
# 7. COMENTÁRIOS
# ══════════════════════════════════════════════════════════════════
print("\n💬 Adicionando comentários...")
token = login("admin@zeladoria.com", "admin123") or token

COMENTARIOS = [
    "Equipe enviada para verificação. Prazo: 48h.",
    "Material solicitado ao almoxarifado.",
    "Serviço concluído pela equipe de campo.",
    "Prioridade elevada após vistoria técnica.",
    "Secretaria notificada formalmente.",
    "Aguardando liberação de verba para execução.",
    "Obra programada para a próxima semana.",
    "Equipe realizando reparo emergencial no local.",
]

for cid in chamado_ids[:20]:
    for _ in range(random.randint(1, 2)):
        api("POST", f"/chamados/{cid}/comentarios", {
            "texto": random.choice(COMENTARIOS),
            "tipo": random.choice(["atualizacao", "observacao"]),
            "visivel_cidadao": random.choice([True, False]),
        })
        time.sleep(0.2)
ok("Comentários adicionados")

# ══════════════════════════════════════════════════════════════════
# 8. PROPOSTAS
# ══════════════════════════════════════════════════════════════════
print("\n🗳️ Criando propostas participativas...")

PROPOSTAS = [
    ("Ciclovia na Av. Almirante Barroso",          15000000, "Infraestrutura",   "Umarizal"),
    ("Revitalização da Praça da República",          800000, "Praças e Parques", "Nazaré"),
    ("Câmeras de segurança no Ver-o-Peso",           350000, "Segurança",        "Cidade Velha"),
    ("Arborização urbana — 5000 mudas",              200000, "Meio Ambiente",    "Marco"),
    ("Academia ao ar livre no Umarizal",             120000, "Esporte e Lazer",  "Umarizal"),
    ("Alargamento de calçada na Trav. Mauriti",       90000, "Acessibilidade",   "Batista Campos"),
    ("Iluminação LED no Entroncamento",              450000, "Iluminação",       "Entroncamento"),
    ("Centro comunitário para o Guamá",              650000, "Social",           "Guamá"),
    ("Reforma do mercado do Jurunas",                380000, "Infraestrutura",   "Jurunas"),
    ("Parque linear no igarapé Tucunduba",          1200000, "Meio Ambiente",    "Guamá"),
]

prop_ids = []
for titulo, custo, cat, bairro in PROPOSTAS:
    r = api("POST", "/transparencia/propostas", {
        "titulo": titulo,
        "descricao": f"Proposta para {titulo.lower()}. Beneficiará milhares de moradores de Belém.",
        "custo_estimado": custo, "categoria": cat, "bairro": bairro,
    })
    if r and r.ok:
        pid = r.json().get("id")
        if pid:
            prop_ids.append(pid)
            ok(f"{titulo[:48]}")
    time.sleep(0.4)

# Votos
tok_cid = login("cidadao@zeladoria.com", "cidadao123")
if tok_cid and prop_ids:
    for pid in random.sample(prop_ids, min(6, len(prop_ids))):
        api("POST", f"/transparencia/propostas/{pid}/votar", tok=tok_cid)
        time.sleep(0.2)
    ok(f"Votos registrados em {min(6, len(prop_ids))} propostas")

# ══════════════════════════════════════════════════════════════════
# 9. CONTRATOS
# ══════════════════════════════════════════════════════════════════
print("\n📄 Criando contratos...")
token = login("admin@zeladoria.com", "admin123") or token

CONTRATOS = [
    ("2024/001", "Construtora Belém Ltda",      "Manutenção de vias públicas",          2500000, "ativo",     48),
    ("2024/002", "EcoCidade Ambiental S.A",      "Coleta e destinação de resíduos",      1800000, "ativo",     24),
    ("2024/003", "LuzBelém Iluminação",          "Instalação e manutenção LED",           950000, "ativo",     72),
    ("2024/004", "Verde Pará Paisagismo",         "Poda e arborização urbana",             320000, "ativo",     48),
    ("2024/005", "Pavimenta Norte Ltda",          "Pavimentação de vias secundárias",     3200000, "ativo",     72),
    ("2024/006", "AquaBelém Saneamento",          "Manutenção da rede de drenagem",       1100000, "encerrado", 48),
    ("2024/007", "Digital Trânsito S.A",          "Sinalização e semáforos",               780000, "ativo",     24),
    ("2023/012", "Engenharia Amazônica",          "Reforma de pontes e passarelas",       4500000, "encerrado", 96),
]

for num, forn, obj, valor, status, sla in CONTRATOS:
    r = api("POST", "/contratos/", {
        "numero": num, "fornecedor": forn, "objeto": obj,
        "valor": valor, "status": status, "sla_horas": sla,
        "data_inicio": (datetime.now() - timedelta(days=random.randint(30,365))).isoformat(),
        "data_fim":    (datetime.now() + timedelta(days=random.randint(30,730))).isoformat(),
    })
    if r and r.ok:
        ok(f"Contrato {num}")
    else:
        code = r.status_code if r else "timeout"
        err(f"Contrato {num}: {code} {r.text[:50] if r else ''}")
    time.sleep(0.4)

# ══════════════════════════════════════════════════════════════════
# 10. SENSORES IoT
# ══════════════════════════════════════════════════════════════════
print("\n📡 Registrando sensores IoT...")

SENSORES = [
    ("Sensor Alagamento Sacramenta",   "alagamento",   "Sacramenta",    True),
    ("Sensor Alagamento Jurunas",      "alagamento",   "Jurunas",       True),
    ("Sensor Qualidade Ar Ver-o-Peso", "qualidade_ar", "Cidade Velha",  True),
    ("Sensor Qualidade Ar Entroncam.", "qualidade_ar", "Entroncamento", False),
    ("Sensor Iluminação Umarizal",     "iluminacao",   "Umarizal",      True),
    ("Sensor Temperatura Nazaré",      "temperatura",  "Nazaré",        True),
    ("Sensor Nível Rio Guamá",         "alagamento",   "Guamá",         True),
    ("Sensor Qualidade Ar Pedreira",   "qualidade_ar", "Pedreira",      False),
]

for nome, tipo, bairro, ativo in SENSORES:
    lat, lng = random.choice(COORDS)
    r = api("POST", "/integracoes/sensores", {
        "nome": nome, "tipo": tipo, "bairro": bairro, "ativo": ativo,
        "latitude":  round(lat + random.uniform(-0.003, 0.003), 6),
        "longitude": round(lng + random.uniform(-0.003, 0.003), 6),
    })
    if r and r.ok:
        ok(f"{nome}")
    else:
        err(f"{nome}: {r.status_code if r else 'timeout'}")
    time.sleep(0.3)

# ══════════════════════════════════════════════════════════════════
# 11. GPS EQUIPES
# ══════════════════════════════════════════════════════════════════
print("\n📍 Simulando GPS das equipes...")
for email, senha in [("equipe@zeladoria.com","equipe123"), ("equipe2@zeladoria.com","equipe123")]:
    tok = login(email, senha)
    if tok:
        lat, lng = random.choice(COORDS)
        api("POST", "/geo/equipes/localizacao", {
            "latitude":  round(lat + random.uniform(-0.005,0.005), 6),
            "longitude": round(lng + random.uniform(-0.005,0.005), 6),
            "precisao_m": random.uniform(5, 20),
            "velocidade": random.uniform(0, 40),
            "em_servico": True,
            "bateria": random.randint(60, 100),
        }, tok=tok)
        ok(f"GPS: {email}")
    time.sleep(0.5)

# ══════════════════════════════════════════════════════════════════
print(f"""
╔═══════════════════════════════════════════╗
║          SEED CONCLUÍDO! 🎉              ║
╠═══════════════════════════════════════════╣
║  📋 {len(chamado_ids):2d} chamados criados              ║
║  🗳️  {len(prop_ids):2d} propostas participativas      ║
║  📄  {len(CONTRATOS):2d} contratos                    ║
║  📡  {len(SENSORES):2d} sensores IoT                ║
╚═══════════════════════════════════════════╝

Credenciais para login:
  admin@zeladoria.com   / admin123
  gestor@zeladoria.com  / gestor123
  equipe@zeladoria.com  / equipe123
  cidadao@zeladoria.com / cidadao123
  seurb@zeladoria.com   / seurb123
""")
