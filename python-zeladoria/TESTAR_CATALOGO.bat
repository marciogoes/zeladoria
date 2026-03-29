@echo off
chcp 65001 >nul
echo.
echo ========================================================
echo    TESTANDO API DO CATALOGO
echo    Sistema de Zeladoria Urbana
echo ========================================================
echo.
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate

echo.
echo [INFO] Testando endpoints...
echo.

python -c "import requests; r = requests.get('http://localhost:8001/api/catalogo'); print('Total de servicos:', len(r.json()) if r.status_code == 200 else 'ERRO: ' + str(r.status_code))"

echo.
echo ========================================================
echo.
echo Acesse no navegador:
echo.
echo   API Catalogo:
echo   http://localhost:8001/api/catalogo
echo.
echo   Catalogo Visual:
echo   http://localhost:8001/static/catalogo.html
echo.
echo   Documentacao:
echo   http://localhost:8001/docs
echo.
echo ========================================================
echo.
pause
