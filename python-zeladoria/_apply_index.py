import os, base64, sys

d = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(d, 'frontend', 'index.html')

try:
    p1 = open(os.path.join(d, '_p1.b64')).read().strip()
    p2 = open(os.path.join(d, '_p2.b64')).read().strip()
    content = base64.b64decode(p1 + p2).decode('utf-8')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {len(content)} chars -> {out}')
    print(f'  Paginacao: {"_totalPaginas" in content}')
    print(f'  Timeline:  {"mostrarTimeline" in content}')
    print(f'  Dashboard: {"stat-tempo-medio" in content}')
    for fn in ['_p1.b64', '_p2.b64', '_apply_index.py']:
        fp = os.path.join(d, fn)
        if os.path.exists(fp): os.remove(fp)
    print('Pronto! Faca git add . && git commit && git push')
except Exception as e:
    print(f'ERRO: {e}')
    sys.exit(1)
