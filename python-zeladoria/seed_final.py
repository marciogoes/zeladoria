"""
seed_final.py — Seed completo usando zeloadmin como admin
Execute: python seed_final.py
"""
import requests, random, time
from datetime import datetime, timedelta

BASE = "https://zeladoria-backend-production.up.railway.app/api"
H    = {"Content-Type": "application/json"}

def login(email, senha):
    r = requests.post(f"{BASE}/auth/login", json={"email": email, "senha": senha}, headers=H, timeout=15)
    if r.ok:
        d = r.json()
        return d.get("access_token") or d.get("token")
    return None

def api(method, endpoint, data=None, tok=None):
    h = {**H}
    if tok: h["Authorization"] = f"Bearer {tok}"
    fn = {"GET": requests.get, "POST": requests.post, "PATCH": requests.patch}[method]
    kw = {"headers": h, "timeout": 15}
    if data is not None: kw["json"] = data
    try:
        r = fn(f"{BASE}{endpoint}", **kw)
        return r
    except Exception as e:
        print(f"  ⚠️  {e}")
        return None

def reg(u, tok_admin):
    """Tenta registrar; se existir, tenta trocar senha via endpoint admin (se disponível)."""
    r = requests.post(f"{BASE}/auth/register", json=u, headers=H, timeout=15)
    if r.status_code in (200, 201):
        print(f"  ✅ Criado: {u['email']}")
        return True
    elif r.status_code == 429:
        print(f"  ⏳ Rate limit: {u['email']} — aguardando 12s...")
        time.sleep(12)
        r2 = requests.post(f"{BASE}/auth/register", json=u, headers=H, timeout=15)
        if r2.status_code in (200, 201):
            print(f"  ✅ Criado: {u['email']}")
        else:
            print(f"  ⚠️  {u['email']} → {r2.status_code}")
    elif r.status_code == 400:
        print(f"  ℹ️  Já existe: {u['email']}")
    else:
        print(f"  ❌ {u['email']} → {r.status_code}: {r.text[:60]}")
    return True

# ═══════════════════════════════════════════════════
print("🔑 Login como zeloadmin...")
TOK = None
for tentativa in range(4):
    TOK = login("zeloadmin@zeladoria.com", "Zelo@2026")
    if TOK:
        print("  ✅ OK")
        break
    import re as _re, requests as _rq
    r_test = _rq.post(f"{BASE}/auth/login",
                      json={"email":"zeloadmin@zeladoria.com","senha":"Zelo@2026"},
                      headers=H, timeout=10)
    detail = r_test.json().get("detail","") if r_test.status_code != 200 else ""
    if "429" in str(r_test.status_code) or "Muitas" in detail:
        print(f"  ⏳ Rate limit ativo — aguardando 65s (tentativa {tentativa+1}/4)...")
        time.sleep(65)
    else:
        print(f"  ❌ Falha: {r_test.status_code} {detail}")
        print("  Crie o usuário rodando: python reset_admin.py")
        exit(1)
if not TOK:
    print("❌ Rate limit persistente. Aguarde 15 min e rode novamente.")
    exit(1)

# ═══════════════════════════════════════════════════
print("\n👥 Registrando usuários...")
USUARIOS = [
    {"nome":"Admin Sistema",        "email":"admin@zeladoria.com",   "senha":"admin123",   "tipo":"admin"},
    {"nome":"Gestor Municipal",      "email":"gestor@zeladoria.com",  "senha":"gestor123",  "tipo":"gestor"},
    {"nome":"Equipe Campo A",        "email":"equipe@zeladoria.com",  "senha":"equipe123",  "tipo":"equipe"},
    {"nome":"Equipe Campo B",        "email":"equipe2@zeladoria.com", "senha":"equipe123",  "tipo":"equipe"},
    {"nome":"Cidadão João",          "email":"cidadao@zeladoria.com", "senha":"cidadao123", "tipo":"cidadao"},
    {"nome":"Maria Silva",           "email":"maria@zeladoria.com",   "senha":"cidadao123", "tipo":"cidadao"},
    {"nome":"Carlos Oliveira",       "email":"carlos@zeladoria.com",  "senha":"cidadao123", "tipo":"cidadao"},
    {"nome":"Ana Costa SEURB",       "email":"seurb@zeladoria.com",   "senha":"seurb123",   "tipo":"secretaria"},
    {"nome":"Pedro Santos SESAN",    "email":"sesan@zeladoria.com",   "senha":"sesan123",   "tipo":"secretaria"},
    {"nome":"Luiza Ferreira SEMOB",  "email":"semob@zeladoria.com",   "senha":"semob123",   "tipo":"secretaria"},
    {"nome":"Roberto Lima SEMMA",    "email":"semma@zeladoria.com",   "senha":"semma123",   "tipo":"secretaria"},
]
for u in USUARIOS:
    reg(u, TOK)
    time.sleep(2)

# ═══════════════════════════════════════════════════
print("\n📂 Categorias e bairros...")
r = api("GET", "/categorias", tok=TOK)
cat_ids = [c["id"] for c in r.json()] if r and r.ok else []
print(f"  {len(cat_ids)} categorias")

r = api("GET", "/bairros", tok=TOK)
bairro_ids = [b["id"] for b in r.json()] if r and r.ok else []
print(f"  {len(bairro_ids)} bairros")

# ═══════════════════════════════════════════════════
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

COORDS = [(-1.4558,-48.4902),(-1.4780,-48.5001),(-1.4200,-48.4600),
          (-1.4900,-48.4700),(-1.4650,-48.5100),(-1.4450,-48.5200),
          (-1.5000,-48.4800),(-1.4300,-48.4900),(-1.4700,-48.4400),(-1.4100,-48.5000)]
STATUS_C = ["aberto","aberto","aberto","em_andamento","em_andamento","resolvido","cancelado"]
chamado_ids = []

for i, (titulo, prio) in enumerate(TITULOS):
    # Renova token a cada 8 chamados
    if i % 8 == 0 and i > 0:
        novo = login("zeloadmin@zeladoria.com", "Zelo@2026")
        if novo: TOK = novo

    lat, lng = random.choice(COORDS)
    payload = {
        "titulo": titulo,
        "descricao": f"Problema identificado pelos moradores: {titulo}. Solicitamos verificação urgente.",
        "prioridade": prio,
        "latitude":  round(lat + random.uniform(-0.005, 0.005), 6),
        "longitude": round(lng + random.uniform(-0.005, 0.005), 6),
        "endereco": f"Rua {random.choice(['das Flores','do Sol','da Paz','Principal'])}, {random.randint(100,2000)} - Belém/PA",
    }
    if cat_ids:    payload["categoria_id"] = random.choice(cat_ids)
    if bairro_ids: payload["bairro_id"]    = random.choice(bairro_ids)

    r = api("POST", "/chamados", payload, tok=TOK)
    if r and r.ok:
        cid = r.json().get("id")
        chamado_ids.append(cid)
        print(f"  [{i+1:02d}/30] ✅ {titulo[:48]}")
    else:
        code = r.status_code if r else "timeout"
        print(f"  [{i+1:02d}/30] ❌ {code}: {r.text[:60] if r else ''}")
    time.sleep(0.4)

print(f"\n  Total: {len(chamado_ids)} chamados criados")

# ═══════════════════════════════════════════════════
print("\n🔄 Atualizando status...")
TOK = login("zeloadmin@zeladoria.com", "Zelo@2026") or TOK
for i, cid in enumerate(chamado_ids):
    s = STATUS_C[i % len(STATUS_C)]
    if s != "aberto":
        api("PATCH", f"/chamados/{cid}/status", {"status": s}, tok=TOK)
        time.sleep(0.2)
print("  ✅ Feito")

# ═══════════════════════════════════════════════════
print("\n⭐ Avaliando chamados resolvidos...")
tok_cid = login("cidadao@zeladoria.com", "cidadao123")
if tok_cid:
    FRASES = ["Ótimo atendimento!","Resolveram rapidamente.","Bom serviço!","Satisfeito.","Profissional."]
    for i, cid in enumerate(chamado_ids):
        if STATUS_C[i % len(STATUS_C)] == "resolvido":
            api("POST", f"/chamados/{cid}/avaliar",
                {"avaliacao": random.randint(3,5), "comentario_avaliacao": random.choice(FRASES)},
                tok=tok_cid)
            time.sleep(0.3)
    print("  ✅ Avaliações registradas")
else:
    print("  ⚠️  cidadao ainda rate-limited, pulando avaliações")

# ═══════════════════════════════════════════════════
print("\n💬 Comentários internos...")
TOK = login("zeloadmin@zeladoria.com", "Zelo@2026") or TOK
CMTS = ["Equipe enviada. Prazo: 48h.","Material solicitado.","Serviço concluído.",
        "Vistoria realizada.","Aguardando verba.","Reparo emergencial em andamento."]
for cid in chamado_ids[:20]:
    for _ in range(random.randint(1,2)):
        api("POST", f"/chamados/{cid}/comentarios",
            {"texto": random.choice(CMTS), "tipo": random.choice(["atualizacao","observacao"]),
             "visivel_cidadao": random.choice([True,False])}, tok=TOK)
        time.sleep(0.2)
print("  ✅ Feito")

# ═══════════════════════════════════════════════════
print("\n🗳️ Propostas participativas...")
PROPOSTAS = [
    ("Ciclovia na Av. Almirante Barroso",     15000000,"Infraestrutura","Umarizal"),
    ("Revitalização da Praça da República",      800000,"Praças e Parques","Nazaré"),
    ("Câmeras de segurança no Ver-o-Peso",       350000,"Segurança","Cidade Velha"),
    ("Arborização urbana — 5000 mudas",          200000,"Meio Ambiente","Marco"),
    ("Academia ao ar livre no Umarizal",         120000,"Esporte e Lazer","Umarizal"),
    ("Iluminação LED no Entroncamento",          450000,"Iluminação","Entroncamento"),
    ("Centro comunitário para o Guamá",          650000,"Social","Guamá"),
    ("Reforma do mercado do Jurunas",            380000,"Infraestrutura","Jurunas"),
    ("Parque linear no igarapé Tucunduba",      1200000,"Meio Ambiente","Guamá"),
    ("Acessibilidade na Trav. Mauriti",           90000,"Acessibilidade","Batista Campos"),
]
prop_ids = []
for titulo, custo, cat, bairro in PROPOSTAS:
    r = api("POST", "/transparencia/propostas",
            {"titulo": titulo, "descricao": f"Proposta para melhorar {bairro}.",
             "custo_estimado": custo, "categoria": cat, "bairro": bairro}, tok=TOK)
    if r and r.ok:
        pid = r.json().get("id")
        if pid: prop_ids.append(pid)
        print(f"  ✅ {titulo[:48]}")
    time.sleep(0.4)

# Votos
tok_cid = login("cidadao@zeladoria.com", "cidadao123")
if tok_cid and prop_ids:
    for pid in random.sample(prop_ids, min(6, len(prop_ids))):
        api("POST", f"/transparencia/propostas/{pid}/votar", tok=tok_cid)
        time.sleep(0.2)

# ═══════════════════════════════════════════════════
print("\n📄 Contratos...")
TOK = login("zeloadmin@zeladoria.com", "Zelo@2026") or TOK
CONTRATOS = [
    ("2024/001","Construtora Belém Ltda",   "Manutenção de vias públicas",       2500000,"ativo",    48),
    ("2024/002","EcoCidade Ambiental S.A",  "Coleta e destinação de resíduos",   1800000,"ativo",    24),
    ("2024/003","LuzBelém Iluminação",      "Instalação e manutenção LED",        950000,"ativo",    72),
    ("2024/004","Verde Pará Paisagismo",    "Poda e arborização urbana",          320000,"ativo",    48),
    ("2024/005","Pavimenta Norte Ltda",     "Pavimentação de vias secundárias",  3200000,"ativo",    72),
    ("2024/006","AquaBelém Saneamento",     "Manutenção da rede de drenagem",    1100000,"encerrado",48),
    ("2024/007","Digital Trânsito S.A",     "Sinalização e semáforos",            780000,"ativo",    24),
    ("2023/012","Engenharia Amazônica",     "Reforma de pontes e passarelas",    4500000,"encerrado",96),
]
for num, forn, obj, valor, status, sla in CONTRATOS:
    r = api("POST", "/contratos/", {
        "numero":num,"fornecedor":forn,"objeto":obj,"valor":valor,
        "status":status,"sla_horas":sla,
        "data_inicio":(datetime.now()-timedelta(days=random.randint(30,365))).isoformat(),
        "data_fim":   (datetime.now()+timedelta(days=random.randint(30,730))).isoformat(),
    }, tok=TOK)
    print(f"  {'✅' if r and r.ok else '❌'} Contrato {num}")
    time.sleep(0.4)

# ═══════════════════════════════════════════════════
print("\n📡 Sensores IoT...")
SENSORES = [
    ("Sensor Alagamento Sacramenta",  "alagamento",  "Sacramenta",   True),
    ("Sensor Alagamento Jurunas",     "alagamento",  "Jurunas",      True),
    ("Sensor Qualidade Ar Ver-o-Peso","qualidade_ar","Cidade Velha", True),
    ("Sensor Iluminação Umarizal",    "iluminacao",  "Umarizal",     True),
    ("Sensor Temperatura Nazaré",     "temperatura", "Nazaré",       True),
    ("Sensor Nível Rio Guamá",        "alagamento",  "Guamá",        True),
    ("Sensor Qualidade Ar Pedreira",  "qualidade_ar","Pedreira",     False),
    ("Sensor Qualidade Ar Entroncam.","qualidade_ar","Entroncamento",False),
]
for nome, tipo, bairro, ativo in SENSORES:
    lat, lng = random.choice(COORDS)
    r = api("POST", "/integracoes/sensores", {
        "nome":nome,"tipo":tipo,"bairro":bairro,"ativo":ativo,
        "latitude": round(lat+random.uniform(-0.003,0.003),6),
        "longitude":round(lng+random.uniform(-0.003,0.003),6),
    }, tok=TOK)
    print(f"  {'✅' if r and r.ok else '❌'} {nome}")
    time.sleep(0.3)

# ═══════════════════════════════════════════════════
print("\n📍 GPS das equipes...")
for email, senha in [("equipe@zeladoria.com","equipe123"),("equipe2@zeladoria.com","equipe123")]:
    tok = login(email, senha)
    if tok:
        lat, lng = random.choice(COORDS)
        api("POST","/geo/equipes/localizacao",{
            "latitude": round(lat+random.uniform(-0.005,0.005),6),
            "longitude":round(lng+random.uniform(-0.005,0.005),6),
            "precisao_m":random.uniform(5,20),"velocidade":random.uniform(0,40),
            "em_servico":True,"bateria":random.randint(60,100),
        }, tok=tok)
        print(f"  ✅ GPS: {email}")
    else:
        print(f"  ⚠️  {email} rate-limited, pulando GPS")
    time.sleep(1)

print(f"""
╔═══════════════════════════════════════════╗
║          SEED CONCLUÍDO! 🎉              ║
╠═══════════════════════════════════════════╣
║  📋 {len(chamado_ids):2d} chamados criados              ║
║  🗳️  {len(prop_ids):2d} propostas                     ║
║  📄  {len(CONTRATOS):2d} contratos                    ║
║  📡  {len(SENSORES):2d} sensores IoT                ║
╚═══════════════════════════════════════════╝

✅ Login agora com:
   zeloadmin@zeladoria.com / Zelo@2026  (Admin)
   equipe@zeladoria.com   / equipe123   (Equipe)
   cidadao@zeladoria.com  / cidadao123  (Cidadão)
""")
