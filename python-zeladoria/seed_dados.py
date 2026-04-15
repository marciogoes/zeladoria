"""
seed_dados.py — Cria apenas DADOS (chamados, propostas, contratos, sensores)
Usa zeloadmin que já existe. Pula registro de usuários.
Execute: python seed_dados.py
"""
import requests, random, time
from datetime import datetime, timedelta

BASE = "https://zeladoria-backend-production.up.railway.app/api"
H = {"Content-Type": "application/json"}

def login(email, senha):
    try:
        r = requests.post(f"{BASE}/auth/login", json={"email":email,"senha":senha}, headers=H, timeout=10)
        if r.ok: return r.json().get("access_token")
    except: pass
    return None

def api(method, endpoint, data=None, tok=None):
    h = {**H, **({"Authorization":f"Bearer {tok}"} if tok else {})}
    fn = {"GET":requests.get,"POST":requests.post,"PATCH":requests.patch}[method]
    try:
        r = fn(f"{BASE}{endpoint}", json=data, headers=h, timeout=10)
        return r
    except Exception as e:
        print(f"    ⚠️ timeout/erro: {e}")
        return None

# ── Login ────────────────────────────────────────────────────
print("🔑 Login como zeloadmin...")
TOK = login("zeloadmin@zeladoria.com", "Zelo@2026")
if not TOK:
    print("❌ Rate limit ou conta não existe. Aguarde 15min e tente novamente.")
    exit(1)
print("  ✅ OK")

# ── Categorias e bairros ─────────────────────────────────────
r = api("GET", "/categorias", tok=TOK)
cat_ids = [c["id"] for c in r.json()] if r and r.ok else []
r = api("GET", "/bairros", tok=TOK)
bairro_ids = [b["id"] for b in r.json()] if r and r.ok else []
print(f"  📂 {len(cat_ids)} categorias, {len(bairro_ids)} bairros")

# ── Chamados ─────────────────────────────────────────────────
print("\n📋 Criando chamados...")
TITULOS = [
    ("Buraco profundo na calçada prejudica pedestres",     "baixa"),
    ("Iluminação pública apagada há 3 semanas",            "media"),
    ("Lixo acumulado próximo à escola municipal",          "alta"),
    ("Árvore caída bloqueando via principal",              "critica"),
    ("Vazamento de esgoto na rua principal",               "alta"),
    ("Calçada danificada por raízes de árvore",           "baixa"),
    ("Poda urgente de árvore sobre fiação elétrica",      "critica"),
    ("Bueiro entupido causando alagamento",                "alta"),
    ("Placa de trânsito danificada na rotatória",         "media"),
    ("Faixa de pedestre apagada em via movimentada",      "media"),
    ("Lâmpada queimada na praça da comunidade",           "baixa"),
    ("Entulho irregular depositado em área pública",      "media"),
    ("Buraco na pista causa acidentes frequentes",        "critica"),
    ("Semáforo com defeito no cruzamento central",        "alta"),
    ("Calçamento destruído por obras sem reparo",         "media"),
    ("Alagamento recorrente após chuvas no bairro",       "alta"),
    ("Poste inclinado oferece risco à população",         "critica"),
    ("Lixo em terreno baldio gera foco de dengue",       "alta"),
    ("Meio-fio quebrado dificulta acessibilidade",        "baixa"),
    ("Galeria pluvial obstruída pela vegetação",          "media"),
    ("Praça com brinquedos danificados e enferrujados",   "media"),
    ("Via sem pavimentação dificulta mobilidade",         "baixa"),
    ("Esgoto a céu aberto próximo a residências",        "critica"),
    ("Sinalização viária apagada na saída da cidade",     "media"),
    ("Árvore doente com risco de queda iminente",         "alta"),
    ("Pista com ondulações perigosas p/ motociclistas",   "media"),
    ("Falta de rampas de acessibilidade na calçada",     "baixa"),
    ("Container de lixo transbordando há dias",           "alta"),
    ("Buraco no meio da avenida sem sinalização",         "critica"),
    ("Mato alto em área pública atraindo animais",       "baixa"),
]
COORDS = [(-1.4558,-48.4902),(-1.4780,-48.5001),(-1.4200,-48.4600),
          (-1.4900,-48.4700),(-1.4650,-48.5100),(-1.4450,-48.5200),
          (-1.5000,-48.4800),(-1.4300,-48.4900),(-1.4700,-48.4400),(-1.4100,-48.5000)]
STATUS_C = ["aberto","aberto","aberto","em_andamento","em_andamento","resolvido","cancelado"]
chamado_ids = []

for i, (titulo, prio) in enumerate(TITULOS):
    if i % 10 == 0 and i > 0:
        novo = login("zeloadmin@zeladoria.com","Zelo@2026")
        if novo: TOK = novo
    lat,lng = random.choice(COORDS)
    payload = {
        "titulo": titulo,
        "descricao": f"Problema identificado pelos moradores: {titulo}.",
        "prioridade": prio,
        "latitude":  str(round(lat+random.uniform(-0.005,0.005),6)),
        "longitude": str(round(lng+random.uniform(-0.005,0.005),6)),
        "endereco": f"Rua {random.choice(['das Flores','do Sol','da Paz','Principal'])}, {random.randint(100,2000)} - Belém/PA",
        "categoria_id": str(random.choice(cat_ids)) if cat_ids else "1",
        "bairro_id":    str(random.choice(bairro_ids)) if bairro_ids else "1",
    }

    # /chamados exige multipart/form-data (usa Form() no FastAPI)
    h_form = {"Authorization": f"Bearer {TOK}"}
    try:
        r = requests.post(f"{BASE}/chamados", data=payload, headers=h_form, timeout=15)
    except Exception as e:
        print(f"    ⚠️ {e}")
        r = None
    if r and r.ok:
        cid = r.json().get("id")
        chamado_ids.append(cid)
        print(f"  [{i+1:02d}/30] ✅ {titulo[:45]}")
    else:
        code = r.status_code if r else "timeout"
        print(f"  [{i+1:02d}/30] ❌ {code}")
    time.sleep(0.5)

print(f"\n  ✅ {len(chamado_ids)} chamados criados")

# ── Status dos chamados ──────────────────────────────────────
print("\n🔄 Atualizando status...")
TOK = login("zeloadmin@zeladoria.com","Zelo@2026") or TOK
for i,cid in enumerate(chamado_ids):
    s = STATUS_C[i % len(STATUS_C)]
    if s != "aberto":
        api("PATCH", f"/chamados/{cid}/status", {"status":s}, tok=TOK)
        time.sleep(0.3)
print("  ✅ Feito")

# ── Comentários ──────────────────────────────────────────────
print("\n💬 Adicionando comentários...")
TOK = login("zeloadmin@zeladoria.com","Zelo@2026") or TOK
CMTS = ["Equipe enviada. Prazo: 48h.","Material solicitado.",
        "Serviço concluído.","Vistoria realizada.","Aguardando verba."]
for cid in chamado_ids[:15]:
    api("POST", f"/chamados/{cid}/comentarios", {
        "texto": random.choice(CMTS),
        "tipo": random.choice(["atualizacao","observacao"]),
        "visivel_cidadao": True,
    }, tok=TOK)
    time.sleep(0.3)
print("  ✅ Feito")

# ── Propostas ────────────────────────────────────────────────
print("\n🗳️ Criando propostas...")
TOK = login("zeloadmin@zeladoria.com","Zelo@2026") or TOK
PROPOSTAS = [
    ("Ciclovia na Av. Almirante Barroso",    15000000,"Infraestrutura","Umarizal"),
    ("Revitalização da Praça da República",    800000,"Praças e Parques","Nazaré"),
    ("Câmeras de segurança no Ver-o-Peso",     350000,"Segurança","Cidade Velha"),
    ("Arborização urbana — 5000 mudas",        200000,"Meio Ambiente","Marco"),
    ("Academia ao ar livre no Umarizal",       120000,"Esporte e Lazer","Umarizal"),
    ("Iluminação LED no Entroncamento",        450000,"Iluminação","Entroncamento"),
    ("Centro comunitário para o Guamá",        650000,"Social","Guamá"),
    ("Reforma do mercado do Jurunas",          380000,"Infraestrutura","Jurunas"),
    ("Parque linear no igarapé Tucunduba",    1200000,"Meio Ambiente","Guamá"),
    ("Acessibilidade na Trav. Mauriti",         90000,"Acessibilidade","Batista Campos"),
]
prop_ids = []
for titulo,custo,cat,bairro in PROPOSTAS:
    r = api("POST","/transparencia/propostas",{
        "titulo":titulo,"descricao":f"Proposta para {bairro}.",
        "custo_estimado":custo,"categoria":cat,"bairro":bairro,
    }, tok=TOK)
    if r and r.ok:
        pid = r.json().get("id")
        if pid: prop_ids.append(pid)
        print(f"  ✅ {titulo[:45]}")
    else:
        print(f"  ❌ {r.status_code if r else 'timeout'}")
    time.sleep(0.5)

# Votos nas propostas usando zeloadmin
for pid in random.sample(prop_ids, min(5,len(prop_ids))):
    api("POST",f"/transparencia/propostas/{pid}/votar", tok=TOK)
    time.sleep(0.2)

# ── Contratos ────────────────────────────────────────────────
print("\n📄 Criando contratos...")
TOK = login("zeloadmin@zeladoria.com","Zelo@2026") or TOK
CONTRATOS = [
    ("2024/001","Construtora Belém Ltda",  "Manutenção de vias públicas",      2500000,"ativo",    48),
    ("2024/002","EcoCidade Ambiental S.A", "Coleta e destinação de resíduos",  1800000,"ativo",    24),
    ("2024/003","LuzBelém Iluminação",     "Instalação e manutenção LED",       950000,"ativo",    72),
    ("2024/004","Verde Pará Paisagismo",   "Poda e arborização urbana",         320000,"ativo",    48),
    ("2024/005","Pavimenta Norte Ltda",    "Pavimentação de vias secundárias", 3200000,"ativo",    72),
    ("2024/006","AquaBelém Saneamento",    "Manutenção da rede de drenagem",   1100000,"encerrado",48),
    ("2024/007","Digital Trânsito S.A",    "Sinalização e semáforos",           780000,"ativo",    24),
    ("2023/012","Engenharia Amazônica",    "Reforma de pontes e passarelas",   4500000,"encerrado",96),
]
for num,forn,obj,valor,status,sla in CONTRATOS:
    r = api("POST","/contratos/",{
        "numero":num,"fornecedor":forn,"objeto":obj,"valor":valor,
        "status":status,"sla_horas":sla,
        "data_inicio":(datetime.now()-timedelta(days=random.randint(30,365))).isoformat(),
        "data_fim":   (datetime.now()+timedelta(days=random.randint(30,730))).isoformat(),
    }, tok=TOK)
    print(f"  {'✅' if r and r.ok else '❌'} Contrato {num}")
    time.sleep(0.5)

# ── Sensores IoT ─────────────────────────────────────────────
print("\n📡 Registrando sensores...")
TOK = login("zeloadmin@zeladoria.com","Zelo@2026") or TOK
SENSORES = [
    ("Sensor Alagamento Sacramenta",   "alagamento",  "Sacramenta",    True),
    ("Sensor Alagamento Jurunas",      "alagamento",  "Jurunas",       True),
    ("Sensor Qualidade Ar Ver-o-Peso", "qualidade_ar","Cidade Velha",  True),
    ("Sensor Iluminação Umarizal",     "iluminacao",  "Umarizal",      True),
    ("Sensor Temperatura Nazaré",      "temperatura", "Nazaré",        True),
    ("Sensor Nível Rio Guamá",         "alagamento",  "Guamá",         True),
    ("Sensor Qualidade Ar Pedreira",   "qualidade_ar","Pedreira",      False),
    ("Sensor Qualidade Ar Entroncam.", "qualidade_ar","Entroncamento", False),
]
for nome,tipo,bairro,ativo in SENSORES:
    lat,lng = random.choice(COORDS)
    r = api("POST","/integracoes/sensores",{
        "nome":nome,"tipo":tipo,"bairro":bairro,"ativo":ativo,
        "latitude": round(lat+random.uniform(-0.003,0.003),6),
        "longitude":round(lng+random.uniform(-0.003,0.003),6),
    }, tok=TOK)
    print(f"  {'✅' if r and r.ok else '❌'} {nome}")
    time.sleep(0.4)

print(f"""
╔═════════════════════════════════════╗
║      SEED CONCLUÍDO! 🎉            ║
╠═════════════════════════════════════╣
║  📋 {len(chamado_ids):2d} chamados                  ║
║  🗳️  {len(prop_ids):2d} propostas                  ║
║  📄  {len(CONTRATOS):2d} contratos                 ║
║  📡  {len(SENSORES):2d} sensores IoT             ║
╚═════════════════════════════════════╝

Acesse agora:
  zeloadmin@zeladoria.com / Zelo@2026
""")
