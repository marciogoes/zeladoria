import os, base64

d = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(d, 'frontend', 'index.html')

p1 = open(os.path.join(d, '_idx_p1.b64')).read().strip()
p2 = open(os.path.join(d, '_idx_p2.b64')).read().strip()
content = base64.b64decode(p1 + p2).decode('utf-8')

with open(out, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'index.html escrito: {len(content)} chars -> {out}')
print(f'  Paginacao S17:   {"_totalPaginas" in content}')
print(f'  Timeline S17:    {"mostrarTimeline" in content}')
print(f'  Tempo medio:     {"stat-tempo-medio" in content}')
print(f'  Bugs corrigidos: {"avaliacao: nota, comentario_avaliacao:" in content}')
print()
print('Sprint 17 aplicado com sucesso!')

for fn in ['_idx_p1.b64', '_idx_p2.b64', '_deploy_index.py']:
    fp = os.path.join(d, fn)
    if os.path.exists(fp):
        os.remove(fp)
print('Arquivos temporarios removidos.')
