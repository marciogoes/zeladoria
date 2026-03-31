@echo off
REM ========================================================================
REM ZELÔ - Correção do index.html (Sprint 17)
REM Execute: duplo-clique neste arquivo ou rode no CMD/PowerShell
REM ========================================================================

cd /d "%~dp0"
echo Reconstruindo index.html do Sprint 17...

REM Usar Python para montar a partir dos chunks b64
python -c "
import os, base64, sys
d = r'%~dp0'
out = os.path.join(d, 'frontend', 'index.html')
chunks = []
for i in range(1, 5):
    fp = os.path.join(d, f'_p{i}.b64')
    if not os.path.exists(fp):
        print(f'ERRO: {fp} nao encontrado')
        sys.exit(1)
    chunks.append(open(fp).read().strip())
content = base64.b64decode(''.join(chunks)).decode('utf-8')
with open(out, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'OK: {len(content)} chars escritos em {out}')
print('  Sprint17:', '_totalPaginas' in content)
for i in range(1, 5):
    fp = os.path.join(d, f'_p{i}.b64')
    if os.path.exists(fp): os.remove(fp)
os.remove(os.path.join(d, '_CORRIGIR_INDEX.bat'))
print('Arquivos temporarios removidos.')
print()
print('AGORA EXECUTE:')
print('  git add frontend/index.html')
print('  git commit -m \"fix: sprint17 index.html\"')  
print('  git push')
"
if %ERRORLEVEL% NEQ 0 (
    echo ERRO ao executar Python. Tente: python _FIX_NOW.py
    pause
) else (
    echo.
    echo SUCESSO! index.html corrigido.
    echo Execute: git add frontend\index.html ^&^& git commit -m "fix: sprint17" ^&^& git push
    pause
)
