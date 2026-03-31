"""
EXECUTAR NO POWERSHELL:
  cd C:\Users\marci\OneDrive\Documentos\Projetos\zeladoria\python-zeladoria
  python _FIX_NOW.py

Este script reconstroi o index.html correto (Sprint 17) a partir dos arquivos _p1.b64 a _p4.b64.
Apos executar, faca:
  git add frontend\index.html
  git commit -m "fix: sprint17 index.html"
  git push
"""
import os, base64, sys

d = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(d, 'frontend', 'index.html')

try:
    parts = []
    for i in range(1, 5):
        fn = os.path.join(d, f'_p{i}.b64')
        if not os.path.exists(fn):
            print(f'ERRO: Arquivo {fn} nao encontrado!')
            print('Execute novamente o Claude para gerar os arquivos _p1.b64 a _p4.b64')
            sys.exit(1)
        parts.append(open(fn).read().strip())
    
    content = base64.b64decode(''.join(parts)).decode('utf-8')
    
    # Verificacoes
    checks = {
        'Sprint 17 paginacao': '_totalPaginas' in content,
        'Sprint 17 timeline':  'mostrarTimeline' in content,
        'Sprint 17 tempo medio': 'stat-tempo-medio' in content,
        'Bugs corrigidos': 'avaliacao: nota, comentario_avaliacao:' in content,
        'showDetails unico': content.count('async function showDetails') == 1,
        'loadChamados unico': content.count('async function loadChamados') == 1,
        'HTML completo': content.endswith('</html>\n'),
    }
    
    todas_ok = all(checks.values())
    
    if todas_ok:
        with open(out, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'index.html escrito com sucesso: {len(content)} chars')
        for k, v in checks.items():
            print(f'  {"OK" if v else "FAIL"} {k}')
        print()
        print('PRONTO! Agora execute:')
        print('  git add frontend\\index.html')
        print('  git commit -m "fix: sprint17 index.html correto"')
        print('  git push')
        
        # Cleanup
        for i in range(1, 5):
            fp = os.path.join(d, f'_p{i}.b64')
            if os.path.exists(fp): os.remove(fp)
        os.remove(os.path.abspath(__file__))
        print('Arquivos temporarios removidos.')
    else:
        print('ERRO: Verificacoes falharam:')
        for k, v in checks.items():
            if not v:
                print(f'  FAIL: {k}')
        sys.exit(1)
        
except Exception as e:
    print(f'ERRO: {e}')
    import traceback; traceback.print_exc()
    sys.exit(1)
