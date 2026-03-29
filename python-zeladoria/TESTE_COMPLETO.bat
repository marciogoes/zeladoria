@echo off
chcp 65001 >nul
echo.
echo ========================================================
echo    TESTE COMPLETO DO SISTEMA
echo ========================================================
echo.

call venv\Scripts\activate

echo [1/3] Testando se backend esta rodando...
curl -s http://localhost:8001/ >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ Backend NAO esta rodando!
    echo    Execute: INICIAR_API_8001.bat
    pause
    exit
)
echo    ✅ Backend rodando!
echo.

echo [2/3] Testando endpoint do catalogo...
curl -s http://localhost:8001/api/catalogo >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ Endpoint catalogo com erro!
) else (
    echo    ✅ Catalogo funcionando!
)
echo.

echo [3/3] Testando arquivos frontend...
if exist "frontend\index.html" (
    echo    ✅ index.html existe
) else (
    echo    ❌ index.html NAO existe
)

if exist "frontend\reclassificacao.js" (
    echo    ✅ reclassificacao.js existe
) else (
    echo    ❌ reclassificacao.js NAO existe
)

if exist "frontend\catalogo.html" (
    echo    ✅ catalogo.html existe
) else (
    echo    ❌ catalogo.html NAO existe
)

echo.
echo ========================================================
echo    URLS PARA TESTAR NO NAVEGADOR:
echo ========================================================
echo.
echo    Sistema: http://localhost:8001/static/index.html
echo    Catalogo: http://localhost:8001/static/catalogo.html
echo    API: http://localhost:8001/docs
echo.
echo ========================================================
echo.
pause
