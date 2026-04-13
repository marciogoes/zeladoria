"""
CORRIGIR_TUDO.py
Corrige API_BASE, botões de acesso rápido e faz push para o Railway.
Execute: python CORRIGIR_TUDO.py
"""
import re, subprocess, sys, os

ARQUIVO = os.path.join(os.path.dirname(__file__), "frontend", "index.html")

print("🔍 Lendo frontend/index.html...")
with open(ARQUIVO, "r", encoding="utf-8") as f:
    conteudo = f.read()

# ── 1. Corrigir API_BASE ──────────────────────────────────────────────────────
BACKEND = "https://zeladoria-backend-production.up.railway.app/api"

# Substitui QUALQUER variante de API_BASE (window.location, http://, etc.)
antes = re.search(r"const API_BASE\s*=\s*['\"]?[^;]+;", conteudo)
print(f"  API_BASE atual: {antes.group() if antes else 'NÃO ENCONTRADO'}")

conteudo = re.sub(
    r"const API_BASE\s*=\s*['\"]?[^;]+;",
    f"const API_BASE = '{BACKEND}';",
    conteudo
)
print(f"  API_BASE novo : const API_BASE = '{BACKEND}';")

# ── 2. Corrigir botões de acesso rápido ──────────────────────────────────────
BOTOES_NOVOS = """                <div class="quick-logins">
                <p>Acesso rápido — demo</p>
                <div class="quick-grid">
                    <button class="quick-btn" data-email="cidadao@zeladoria.com" data-senha="cidadao123">
                        👤 <div><span>Cidadão</span><span class="role">cidadao@zeladoria.com</span></div>
                    </button>
                    <button class="quick-btn" data-email="equipe@zeladoria.com" data-senha="equipe123">
                        👷 <div><span>Equipe</span><span class="role">equipe@zeladoria.com</span></div>
                    </button>
                    <button class="quick-btn" data-email="seurb@zeladoria.com" data-senha="seurb123">
                        🏛️ <div><span>SEURB</span><span class="role">seurb@zeladoria.com</span></div>
                    </button>
                    <button class="quick-btn" data-email="gestor@zeladoria.com" data-senha="gestor123">
                        📊 <div><span>Gestor</span><span class="role">gestor@zeladoria.com</span></div>
                    </button>
                    <button class="quick-btn" data-email="admin@zeladoria.com" data-senha="admin123" style="grid-column: span 2;">
                        🔧 <div><span>Administrador</span><span class="role">admin@zeladoria.com</span></div>
                    </button>
                </div>
            </div>"""

# Substitui o bloco quick-logins inteiro
conteudo = re.sub(
    r'<div class="quick-logins">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>',
    BOTOES_NOVOS + "\n        </div>\n    </div>\n</div>",
    conteudo,
    flags=re.DOTALL
)

# ── 3. Salvar arquivo ─────────────────────────────────────────────────────────
with open(ARQUIVO, "w", encoding="utf-8") as f:
    f.write(conteudo)
print("\n✅ Arquivo salvo com sucesso!")

# Verificação rápida
assert BACKEND in conteudo, "❌ ERRO: API_BASE não foi substituído!"
assert "cidadao@zeladoria.com" in conteudo, "❌ ERRO: Botões não foram atualizados!"
print("✅ API_BASE e botões verificados — ambos corretos")

# ── 4. Git add + commit + push ────────────────────────────────────────────────
print("\n🚀 Fazendo push para o GitHub/Railway...")
pasta = os.path.dirname(__file__)

cmds = [
    ["git", "add", "frontend/index.html"],
    ["git", "commit", "-m", "fix: API_BASE https + botoes acesso rapido corretos"],
    ["git", "push"],
]

for cmd in cmds:
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=pasta, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"  {result.stdout.strip()}")
    if result.returncode != 0:
        if "nothing to commit" in result.stderr or "nothing to commit" in result.stdout:
            print("  (sem mudanças para commitar)")
        else:
            print(f"  ERRO: {result.stderr.strip()}")
    else:
        print(f"  ✅ OK")

print("""
╔═══════════════════════════════════════════╗
║  Push concluído! Railway vai rebuildar.   ║
║  Aguarde ~2 min e recarregue o frontend.  ║
╚═══════════════════════════════════════════╝

Agora rode o seed de dados:
  cd python-zeladoria
  python seed_producao.py
""")
