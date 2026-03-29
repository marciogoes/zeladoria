"""
Script para criar automaticamente todos os arquivos do Sistema de Zeladoria
Execute: python criar_arquivos.py
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Arquivos __init__.py vazios
init_files = [
    "app/models/__init__.py",
    "app/routes/__init__.py",
    "app/schemas/__init__.py",
    "app/database/__init__.py",
    "app/utils/__init__.py",
]

# Criar __init__.py
for file in init_files:
    path = os.path.join(BASE_DIR, file)
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# Auto-generated\n")
    print(f"✓ Criado: {file}")

print("\n✅ Arquivos __init__.py criados!")
print("\n📝 Agora execute:")
print("   pip install -r requirements.txt")
print("   python seed.py")
print("   python main.py")
