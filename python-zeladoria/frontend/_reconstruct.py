"""
Script de reconstrução do index.html
Execute: python _reconstruct.py
"""
import os, base64, zlib

# Conteúdo do index.html em base64+zlib para transferência compacta
# Gerado automaticamente — não edite manualmente
PAYLOAD_B64 = None  # será preenchido pelo Claude

def reconstruir():
    target = os.path.join(os.path.dirname(__file__), 'frontend', 'index.html')
    if PAYLOAD_B64 is None:
        print("ERRO: PAYLOAD_B64 não foi preenchido")
        return
    content = zlib.decompress(base64.b64decode(PAYLOAD_B64)).decode('utf-8')
    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ index.html reconstruído: {len(content)} chars")

if __name__ == '__main__':
    reconstruir()
