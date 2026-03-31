import os, base64, sys

d = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(d, 'frontend', 'index.html')

chunks = []
for i in range(1, 11):
    fp = os.path.join(d, f'_c{i:02d}.b64')
    if not os.path.exists(fp):
        print(f'ERRO: {fp} nao encontrado!')
        sys.exit(1)
    chunks.append(open(fp).read().strip())

content = base64.b64decode(''.join(chunks)).decode('utf-8')

checks = {
    'Sprint17 paginacao': '_totalPaginas' in content,
    'Sprint17 timeline':  'mostrarTimeline' in content,
    'Sprint17 tempo medio': 'stat-tempo-medio' in content,
    'showDetails unico': content.count('async function showDetails') == 1,
    'loadChamados unico': content.count('async function loadChamados') == 1,
    'HTML completo': content.endswith('</html>\n'),
}

if all(checks.values()):
    with open(out, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {len(content)} chars -> {out}')
    for k, v in checks.items():
        print(f'  {"OK" if v else "FAIL"} {k}')
    for i in range(1, 11):
        fp = os.path.join(d, f'_c{i:02d}.b64')
        if os.path.exists(fp): os.remove(fp)
    os.remove(os.path.abspath(__file__))
    for fn in ['_FIX_NOW.py', '_CORRIGIR_INDEX.bat', '_build_index.py', '_deploy_index.py']:
        fp = os.path.join(d, fn)
        if os.path.exists(fp): os.remove(fp)
    print()
    print('PRONTO! Execute agora:')
    print('  git add frontend\\index.html')
    print('  git commit -m "fix: sprint17 index.html"')
    print('  git push')
else:
    print('ERRO nas verificacoes:')
    for k, v in checks.items():
        if not v: print(f'  FAIL: {k}')
    sys.exit(1)
