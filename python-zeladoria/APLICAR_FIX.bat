@echo off
cd /d "%~dp0"
echo Restaurando index.html do git...
git checkout -- frontend/index.html
if errorlevel 1 (
    echo ERRO: git checkout falhou. Certifique-se que o git esta instalado.
    pause
    exit /b 1
)
echo.
echo Executando fix_index.py...
python fix_index.py
if errorlevel 1 (
    echo.
    echo ERRO no fix_index.py. Veja mensagem acima.
    pause
    exit /b 1
)
echo.
echo Fazendo commit...
git add frontend/index.html
git commit -m "fix: index.html reconstruido - 10 funcoes duplicadas removidas, bugs avaliacao corrigidos"
echo.
echo Pronto! Execute 'git push' para enviar ao Railway.
pause
