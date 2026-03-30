import base64, os, sys

# Script gerado automaticamente pelo Claude para reconstruir o index.html
# Execute: python rebuild_index.py
# dentro da pasta python-zeladoria/

d = os.path.dirname(os.path.abspath(__file__))

# Le as 3 partes base64
parts = []
for i in range(1, 4):
    fname = os.path.join(d, f'_idx_b64_p{i}.dat')
    with open(fname) as f:
        parts.append(f.read())

# Decodifica e escreve o index.html
content = base64.b64decode(''.join(parts)).decode('utf-8')
out = os.path.join(d, 'frontend', 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'OK: {len(content)} chars -> {out}')
print('Bugs corrigidos:')
print('  Bug 7  payload avaliacao (avaliacao: nota, comentario_avaliacao)')
print('  Bug 8a c.avaliacao.nota -> c.avaliacao')
print('  Bug 8b c.avaliacao.comentario -> c.comentario_avaliacao')
print('  Bug 9  loadPrevisao style malformado')
print('  10 funcoes JS duplicadas removidas')
print('  loadPropostas restaurada completa')
print('  DOMContentLoaded unico (com .then())')

# Limpa os arquivos temporarios
for i in range(1, 4):
    os.remove(os.path.join(d, f'_idx_b64_p{i}.dat'))
print('Arquivos temporarios removidos.')
