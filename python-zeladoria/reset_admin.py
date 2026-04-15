"""
reset_admin.py — Cria/verifica usuários de acesso via API de produção
Execute: python reset_admin.py
"""
import requests

BASE = "https://zeladoria-backend-production.up.railway.app/api"
H = {"Content-Type": "application/json"}

print("🔍 Testando conexão com o backend de produção...")
r = requests.get(f"{BASE}/categorias", timeout=10)
print(f"  Backend status: {r.status_code} {'✅ OK' if r.ok else '❌ ERRO'}")

print("\n🔑 Testando logins existentes...")
CREDENCIAIS = [
    ("admin@zeladoria.com",   "admin123",   "Admin"),
    ("gestor@zeladoria.com",  "gestor123",  "Gestor"),
    ("equipe@zeladoria.com",  "equipe123",  "Equipe"),
    ("cidadao@zeladoria.com", "cidadao123", "Cidadão"),
    ("seurb@zeladoria.com",   "seurb123",   "SEURB"),
]

token_admin = None
for email, senha, nome in CREDENCIAIS:
    r = requests.post(f"{BASE}/auth/login",
                      json={"email": email, "senha": senha},
                      headers=H, timeout=10)
    if r.ok:
        data = r.json()
        tok = data.get("access_token")
        tipo = data.get("usuario", {}).get("tipo", "?")
        print(f"  ✅ {nome:10} ({email}) → tipo={tipo}")
        if tipo == "admin":
            token_admin = tok
    else:
        print(f"  ❌ {nome:10} ({email}) → {r.status_code}: {r.json().get('detail','')}")

# Se admin falhou, criar novo
if not token_admin:
    print("\n⚠️  Admin não fez login. Tentando criar novo admin...")
    
    # Tenta com email alternativo
    r = requests.post(f"{BASE}/auth/register", json={
        "nome":  "Admin Zelô",
        "email": "zeloadmin@zeladoria.com",
        "senha": "Zelo@2026",
        "tipo":  "admin"
    }, headers=H, timeout=10)
    
    if r.ok:
        print("  ✅ Novo admin criado: zeloadmin@zeladoria.com / Zelo@2026")
        token_admin = r.json().get("access_token")
    else:
        print(f"  ❌ Falha: {r.status_code} {r.text[:100]}")
else:
    print("\n✅ Admin funcionando!")

# Listar usuários se tiver token admin
if token_admin:
    print("\n👥 Usuários no banco de produção:")
    r = requests.get(f"{BASE}/usuarios",
                     headers={**H, "Authorization": f"Bearer {token_admin}"},
                     timeout=10)
    if r.ok:
        for u in r.json():
            print(f"  {u['tipo']:12} {u['email']}")
    
    # Contar chamados
    r = requests.get(f"{BASE}/chamados",
                     headers={**H, "Authorization": f"Bearer {token_admin}"},
                     timeout=10)
    if r.ok:
        data = r.json()
        total = data.get("total") or len(data.get("items", data if isinstance(data, list) else []))
        print(f"\n📋 Total de chamados no banco: {total}")

print("\n" + "="*50)
print("Para entrar no sistema, use as credenciais acima que mostraram ✅")
